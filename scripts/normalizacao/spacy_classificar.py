import argparse
import logging
from datetime import datetime
import os
import json

import spacy
from bs4 import BeautifulSoup
import math

import re


CAMINHO_NORMALIZADOS = "../../dados/normalizados"
CAMINHO_CONVERSAO_MONETARIA = "../../dados/brutos/aasp/conversao-monetaria.json"
CAMINHO_ALBUNS = "../../dados/brutos/guiadosquadrinhos/totais.json"
CAMINHO_MUNICIPIOS = "../../dados/brutos/catarse/cities.json"
CAMINHO_CAMPANHAS = "../../dados/brutos/catarse/campanhas"

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

    def _carregar_json(self, caminho):
        result = {}
        result['sucesso'] = False
        try:
            f = open(caminho, "r")

            # Reading from file
            result['json'] = json.loads(f.read())

            result['sucesso'] = True
        except Exception as e:
            # Lidar com a exceção, se necessário
            log_verbose(self._verbose, f"Erro ao ler o arquivo: {e}")

        finally:
            # Certifique-se de fechar o arquivo, mesmo em caso de exceção
            if f:
                f.close()

            return result

    def _carregar_conversao_monetaria(self):
        result = self._carregar_json(CAMINHO_CONVERSAO_MONETARIA)
        if result['sucesso']:
            self._conversao_monetaria = result['json']
            # existe data de dezembro do ano selecionado?
            ano = str(self._ano * 100 + 12)
            if (not ano in self._conversao_monetaria) or (self._conversao_monetaria[ano] is None):
                log_verbose(self._verbose, f"Não existe conversão de valores monetários em dezembro/{self._ano}")
                result['sucesso'] = False
        return result['sucesso']

    def _carregar_albuns(self):
        result = self._carregar_json(CAMINHO_ALBUNS)
        if result['sucesso']:
            self._albuns = result['json']
        return result['sucesso']

    def _carregar_municipios(self):
        result = self._carregar_json(CAMINHO_MUNICIPIOS)
        if result['sucesso']:
            self._municipios = result['json']
        return result['sucesso']

    def _ajustar_valor(self, ano_ini, mes_ini, valor_ini, ano_fim, mes_fim):
        anomes_ini = str(ano_ini * 100 + mes_ini)
        anomes_fim = str(ano_fim * 100 + mes_fim)

        if valor_ini is None:
            return valor_ini

        return (valor_ini/self._conversao_monetaria[anomes_ini]) * self._conversao_monetaria[anomes_fim]

    def _carregar_campanhas(self):
        if not os.path.exists(CAMINHO_CAMPANHAS):
            return False
        
        caminho_campanhas = os.listdir(CAMINHO_CAMPANHAS)

        quantidade_campanhas = 0

        self._campanhas = []

        # Percorre a lista de arquivos
        for caminho_campanha in caminho_campanhas:
            # Cria o caminho completo para o file
            full_path = os.path.join(CAMINHO_CAMPANHAS, caminho_campanha)
            
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
    
    def _garantir_pastas_normalizacao(self):
        log_verbose(self._verbose, f"Verificando pasta: {CAMINHO_NORMALIZADOS}")
        if not os.path.exists(f"{CAMINHO_NORMALIZADOS}"):
            log_verbose(self._verbose, f"\tCriando pasta: {CAMINHO_NORMALIZADOS}")
            os.mkdir(f"{CAMINHO_NORMALIZADOS}")
        log_verbose(self._verbose, f"Verificando pasta: {CAMINHO_NORMALIZADOS}/{self._ano}")
        if not os.path.exists(f"{CAMINHO_NORMALIZADOS}/{self._ano}"):
            log_verbose(self._verbose, f"\tCriando pasta: {CAMINHO_NORMALIZADOS}/{self._ano}")
            os.mkdir(f"{CAMINHO_NORMALIZADOS}/{self._ano}")

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

    def _ajustar_valores_campanha(self, data):
        # verificar a data de lançamento da campanha
        try:
            data_obj = parse_data(data['detail']['online_date'])
        except ValueError:
            print(f"data original: {data['detail']['online_date']}")
            raise ValueError(f"Formato de data inválido. {data['detail']['online_date']}")

        # ajustar goal e pledged para valor presente
        data['detail']['goal'] = self._ajustar_valor(data_obj.year, data_obj.month, data['detail']['goal'], self._ano, 12)
        data['detail']['pledged'] = self._ajustar_valor(data_obj.year, data_obj.month, data['detail']['pledged'], self._ano, 12)

        # ajustar valores das recompensas
        for reward in data['rewards']:
            reward['minimum_value'] = self._ajustar_valor(data_obj.year, data_obj.month, reward['minimum_value'], self._ano, 12)
            reward['maximum_contributions'] = self._ajustar_valor(data_obj.year, data_obj.month, reward['maximum_contributions'], self._ano, 12)
        return True

    def _ajustar_valor_about(self, data):
        # converter texto de about the HTML (com tags) para TEXT (texto puro, sem marcação)
        about_html = data['detail']['about_html']
        soup = BeautifulSoup(about_html, 'html.parser')
        about_txt = soup.get_text(separator=' ', strip=True)
        data['detail']['about_html'] = about_txt

        return True

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
        about_txt = data['detail']['about_html']

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

        data['spacy_lemmas'] = lemmas
        data['spacy_lemmas_freq'] = freq


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

        data['spacy_entidades'] = entidades

        return True
    
    def _spacy_tfidf(self, data):
        freq = data['spacy_lemmas_freq']
        tfidf = {}
        N = len(self._campanhas)
        for lemma in freq:
            tf = freq[lemma]
            df = self._spacy_doc_freq[lemma]
            tfidf[lemma] = tf * math.log(N/df)
        
        data["tfidf"] = tfidf

        return True

    def _gravar_json_campanhas(self, data):
        arquivo_dados = f"{CAMINHO_NORMALIZADOS}/{self._ano}/{data['detail']['project_id']}.json"
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

        log_verbose(self._verbose, "Carregar arquivos de apoio")
        result = (self._carregar_conversao_monetaria()
                and self._carregar_albuns()
                and self._carregar_municipios()
        )
        log_verbose(self._verbose, "Carregar campanhas")
        result = (result and self._carregar_campanhas()
                and self._garantir_pastas_normalizacao()
                and self._percorrer_campanhas(f'Ajustar valores das campanhas para dez/{self._ano}', self._ajustar_valores_campanha)
                and self._percorrer_campanhas(f'Texto puro', self._ajustar_valor_about)
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