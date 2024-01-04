import argparse
import logging
from datetime import datetime
import os
import json

import spacy
#from bs4 import BeautifulSoup
import math

import re

CAMINHO_NORMALIZADOS = "../../dados/normalizados"
#CAMINHO_CAMPANHAS = "../../dados/brutos/catarse/campanhas"

def log_verbose(verbose, msg):
    if verbose:
        print(msg)
    logging.debug(msg)

def parse_data(data_str):
    try:
        # Tenta converter com fração de segundo
        data_obj = datetime.strptime(data_str, '%Y-%m-%dT%H:%M:%S.%f')
        return data_obj
    except ValueError:
        try:
            # Tenta converter sem fração de segundo
            data_obj = datetime.strptime(data_str, '%Y-%m-%dT%H:%M:%S')
            return data_obj
        except ValueError:
            raise ValueError("Formato de data inválido.")
            
        
class Normalizacao:
    def __init__(self, ano, verbose):
        self._ano = ano
        self._verbose = verbose

    def _carregar_campanhas(self):
        if not os.path.exists(f"{CAMINHO_NORMALIZADOS}/{self._ano}"):
            return False
        
        caminho_campanhas = os.listdir(f"{CAMINHO_NORMALIZADOS}/{self._ano}")

        quantidade_campanhas = 0

        self._campanhas = []

        # Percorre a lista de arquivos
        for caminho_campanha in caminho_campanhas:
            # Cria o caminho completo para o file
            full_path = os.path.join(f"{CAMINHO_NORMALIZADOS}/{self._ano}", caminho_campanha)
            
            # Verifica se o caminho é um arquivo
            if os.path.isfile(full_path) and full_path.endswith(".json"):
                # abrir arquivo
                f = open (full_path, "r")
                
                # ler arquivo como json
                data = json.loads(f.read())

                # fechar arquivo
                f.close()

                # verificar a data de lançamento da campanha
                try:
                    data_obj = parse_data(data['detail']['online_date'])
                except ValueError:
                    print(f"data original: {data['detail']['online_date']}")
                    raise ValueError(f"Formato de data inválido. {data['detail']['online_date']}")

                if data_obj.year <= self._ano:
                    self._campanhas.append(data)
                else:
                    continue

                quantidade_campanhas = quantidade_campanhas + 1

                if self._verbose and ((quantidade_campanhas % 25) == 0):
                    print('.', end='', flush=True)

        print('.')
        log_verbose(self._verbose, f'Campanhas encontradas: {quantidade_campanhas}')
        return True
    
    def _garantir_pastas_spacy(self):
        log_verbose(self._verbose, f"Verificando pasta: {CAMINHO_NORMALIZADOS}/{self._ano}/spacy")
        if not os.path.exists(f"{CAMINHO_NORMALIZADOS}/{self._ano}/spacy"):
            log_verbose(self._verbose, f"\tCriando pasta: {CAMINHO_NORMALIZADOS}/{self._ano}/spacy")
            os.mkdir(f"{CAMINHO_NORMALIZADOS}/{self._ano}/spacy")

        return True

    def _percorrer_campanhas(self, msg, funcao):
        log_verbose(self._verbose, msg)
        quantidade_campanhas = 0
        res = True
        for data in self._campanhas:

            res = funcao(data)
            if not res:
                break

            quantidade_campanhas = quantidade_campanhas + 1

            if self._verbose and ((quantidade_campanhas % 25) == 0):
                print('.', end='', flush=True)

        print('.')
        return res

    def _spacy_token_valido(self, text, pos):
        return (
            not(' ' in text) 
            and not ('_' in text) 
            and (text != 'à') 
            and (text != 'às') 
            and (text != 'a') 
            and (text != 'as') 
            and (text != 'o') 
            and (text != 'os') 
            and (text != 'para') 
            and (text != 'de') 
            and (pos == 'NOUN') 
            and re.match(r'^\w+$', text.lower())
        )

    def _spacy_processar(self, data):
        about_txt = data['detail']['about_txt']

        # Processamento do texto com spaCy
        doc = self._nlp(about_txt)

        # Obtenha os lemmas dos tokens que são NOUN (substantivo)
        lemmas = [token.lemma_.lower() for token in doc if self._spacy_token_valido(token.text, token.pos_)]

        # Calcular a frequencia dos termos no documento
        freq = {}
        for lemma in lemmas:
            if not (lemma in freq):
                freq[lemma] = 0

                # na primeira ocorrência do termo, contar document_frequency
                if not (lemma in self._spacy_doc_freq):
                    self._spacy_doc_freq[lemma] = 1
                else:
                    self._spacy_doc_freq[lemma] = self._spacy_doc_freq[lemma] + 1

            freq[lemma] = freq[lemma] + 1

        data['lemmas'] = lemmas
        data['lemmas_freq'] = freq


        #entidades
        entidades = {}
        for entity in doc.ents:
            ent = entity.text
            if not(ent in entidades):
                entidades[ent] = 0

                if not(ent in self._spacy_doc_entidades_freq):
                    self._spacy_doc_entidades_freq[ent] = 1
                else:
                    self._spacy_doc_entidades_freq[ent] = self._spacy_doc_entidades_freq[ent]+1

            entidades[ent] = entidades[ent] + 1

        data['entidades'] = entidades

        return True
    
    def _spacy_tfidf(self, data):
        freq = data['lemmas_freq']
        tfidf = {}
        N = len(self._campanhas)
        for lemma in freq:
            tf = freq[lemma]
            df = self._spacy_doc_freq[lemma]
            tfidf[lemma] = tf * math.log(N/df)
        
        data["tfidf"] = tfidf

        return True

    def _gravar_json_campanhas(self, data):
        arquivo_dados = f"{CAMINHO_NORMALIZADOS}/{self._ano}/spacy/{data['detail']['project_id']}.json"
        with open(arquivo_dados, 'w') as arquivo_json:
            json.dump(data, arquivo_json)

        return True
    
    def _gravar_document_frequency(self):
        log_verbose(self._verbose, f"Spacy: frequência dos termos no corpus: {len(self._spacy_doc_freq)}")
        N = len(self._campanhas)
        df = len(self._spacy_doc_freq)
        
        log_verbose(self._verbose, f"Spacy: campanhas: {N}, doc_freq: {df}")
        arquivo_dados = f"{CAMINHO_NORMALIZADOS}/spacy_frequencia_corpus{self._ano}.json"
        with open(arquivo_dados, 'w') as arquivo_json:
            json.dump(self._spacy_doc_freq, arquivo_json)

        log_verbose(self._verbose, f"Spacy: frequências de entidades no no corpus: {len(self._spacy_doc_entidades_freq)}")
        arquivo_dados = f"{CAMINHO_NORMALIZADOS}/spacy_frequencia_entidades_corpus{self._ano}.json"
        with open(arquivo_dados, 'w') as arquivo_json:
            json.dump(self._spacy_doc_entidades_freq, arquivo_json)

        return True

    def executar(self):
        # Carregue o modelo do spaCy para português
        self._nlp = spacy.load('pt_core_news_sm')
        self._spacy_doc_freq = {}
        self._spacy_doc_entidades_freq = {}

        log_verbose(self._verbose, "Carregar campanhas")
        result = True
        result = (result and self._carregar_campanhas()
                and self._garantir_pastas_spacy()
                and self._percorrer_campanhas(f'Spacy - processar', self._spacy_processar)
                and self._percorrer_campanhas(f'Spacy - TF-IDF', self._spacy_tfidf)
                and self._percorrer_campanhas(f'Gravar arquivos normalizados das campanhas', self._gravar_json_campanhas)
                and self._gravar_document_frequency()
        )



if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog = "normalizar",
        description='Padronizar os dados das campanhas para facilitar as análises')
    parser.add_argument('-v', '--verbose',
                    action='store_true')  # on/off flag
    parser.add_argument('-l', '--loglevel', choices=['DEBUG','INFO','WARNING','ERROR','CRITICAL'], required=False)
    # Adiciona o argumento obrigatório -a/--ano
    parser.add_argument('-a', '--ano', type=int, required=True, help='Ano limite para consolidação')
    
    args = parser.parse_args()

    log_level = logging.WARNING
    if args.loglevel == 'CRITICAL':
        log_level = logging.CRITICAL
    elif args.loglevel =='ERROR':
        log_level = logging.ERROR
    elif args.loglevel =='WARNING':
        log_level = logging.WARNING
    elif args.loglevel =='INFO':
        log_level = logging.INFO
    elif args.loglevel =='DEBUG':
        log_level = logging.DEBUG

    if not os.path.exists("log"):
        os.makedirs("log")
    log_filename = f"log/aasp{datetime.today().strftime('%Y%m%d_%H%M%S')}.log"

    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=log_level,
        filename=log_filename,
        datefmt='%Y-%m-%d %H:%M:%S')
    logging.getLogger().setLevel(log_level)

    if args.verbose:
        print(f"Processar campanhas até {args.ano}")
        print(f"ATENÇÃO, os valores monetários serão ajustados para dezembro/{args.ano}")

    norm = Normalizacao(args.ano, args.verbose)
    norm.executar()