import colunas as colunaslib
import argparse
import logging
from datetime import datetime, timedelta
import os
import json

from bs4 import BeautifulSoup

import re
import requests
import uuid

import pandas as pd
from unidecode import unidecode

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.cluster import KMeans
from nltk.corpus import stopwords
import nltk


CAMINHO_NORMALIZADOS = "../../dados/normalizados"
CAMINHO_CONVERSAO_MONETARIA = "../../dados/brutos/aasp/conversao-monetaria.json"
CAMINHO_ALBUNS = "../../dados/brutos/guiadosquadrinhos/totais.json"
CAMINHO_MUNICIPIOS = "../../dados/brutos/catarse/cities.json"
CAMINHO_CAMPANHAS_CATARSE = "../../dados/brutos/catarse/campanhas"
CAMINHO_CAMPANHAS_APOIASE = "../../dados/brutos/apoiase/campanhas"

REGEX_PRIMEIRO_NOME = re.compile(r'^[\w]+$')

from datetime import datetime, timedelta

def calcular_diferenca_dias(data_inicial_str, data_final_str):
    # Converter as strings em objetos datetime
    data_inicial = datetime.fromisoformat(data_inicial_str.replace('Z', ''))
    
    if data_final_str is None or data_final_str == '':
        # Se a data final for None, use a data atual
        data_final = datetime.utcnow()
    else:
        data_final = datetime.fromisoformat(data_final_str.replace('Z', ''))
    
    # Calcular a diferença em dias
    diferenca = data_final - data_inicial
    
    # Extrair a parte dos dias da diferença
    diferenca_em_dias = diferenca.days
    
    return diferenca_em_dias


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

# referência:
# https://github.com/guilhermecgs/genderbr/blob/master/tests/integration/test_genderbr.py            
def obter_dados_ibge_nome(nome, sexo):
    response = requests.get('http://servicodados.ibge.gov.br/api/v2/censos/nomes/' + nome + '?sexo=' + sexo)
    return response.json()


def get_gender(nome):
    if nome == '':
        return None

    freq_f = obter_dados_ibge_nome(nome, 'F')
    freq_m = obter_dados_ibge_nome(nome, 'M')

    if freq_f:
        sum_freq_f = sum(item['frequencia'] for item in freq_f[0]['res'])
    else:
        sum_freq_f = 0

    if freq_m:
        sum_freq_m = sum(item['frequencia'] for item in freq_m[0]['res'])
    else:
        sum_freq_m = 0

    if sum_freq_f > 0 or sum_freq_m > 0:
        return 'F' if sum_freq_f > sum_freq_m else 'M'
    else:
        return None
    
class Normalizacao:
    def __init__(self, ano, verbose):
        self._ano = ano
        self._verbose = verbose
        self._nomes_com_genero = {}

    def _carregar_uf_brasileiras(self):
        self._uf_brasileiras = [
            'AC',  # Acre
            'AL',  # Alagoas
            'AP',  # Amapá
            'AM',  # Amazonas
            'BA',  # Bahia
            'CE',  # Ceará
            'DF',  # Distrito Federal
            'ES',  # Espírito Santo
            'GO',  # Goiás
            'MA',  # Maranhão
            'MT',  # Mato Grosso
            'MS',  # Mato Grosso do Sul
            'MG',  # Minas Gerais
            'PA',  # Pará
            'PB',  # Paraíba
            'PR',  # Paraná
            'PE',  # Pernambuco
            'PI',  # Piauí
            'RJ',  # Rio de Janeiro
            'RN',  # Rio Grande do Norte
            'RS',  # Rio Grande do Sul
            'RO',  # Rondônia
            'RR',  # Roraima
            'SC',  # Santa Catarina
            'SP',  # São Paulo
            'SE',  # Sergipe
            'TO'   # Tocantins
        ]
        return True
    

    def _verificar_genero(self, nome):
        if nome not in self._nomes_com_genero:
            return None

        return self._nomes_com_genero[nome]
    
    def _carregar_arquivos_frequencia_nomes(self):
        self._show_message("> carregando dicionário de nomes")
        # referência: https://brasil.io/dataset/genero-nomes/nomes/
        # baixado em 2024-01-13
        df = pd.read_csv('./nomes.csv')

        # Filtrar as linhas com "ratio" igual a 1.0
        linhas_com_ratio_1 = df[df['ratio'] > 0.75]

        quant = 0
        # Iterar sobre as linhas filtradas e trabalhar com as colunas 'alternative_names' e 'first_name'
        for index, row in linhas_com_ratio_1.iterrows():
            first_name = row['first_name'].lower()
            alternative_names = row['alternative_names']
            genero = row['classification']
            if alternative_names is None or pd.isna(alternative_names):
                alternative_names = ''
            alternative_names = alternative_names.lower().split('|')

            nomes = [first_name]
            if len(alternative_names)>0:
                nomes.extend(alternative_names)
            
            for n in nomes:
                if n not in self._nomes_com_genero:
                    self._nomes_com_genero[n] = genero
            
            quant = quant + 1
            if ( quant > 1000):
                quant = 0
                print('.', flush=True, end='')

        print('')
                    
        return True

    def _carregar_arquivo_padroes(self, caminho_arquivo, cats, precisos, comeca_com, contem):
        # abrir arquivo
        try:
            f = open (caminho_arquivo, "r", encoding="utf8")
            
            # ler arquivo como json
            data = json.loads(f.read())
            estruts = ['full','comeca_com', 'contem']

            for c in cats:
                for t in estruts:
                    data[c][t] = data[c].get(t, [])

                    if t == 'full':
                        precisos[c] = [re.compile(f"^{pat}$") for pat in data[c][t] if pat.strip()]
                    elif t == 'comeca_com':
                        comeca_com[c] = [re.compile(rf"^{pat}(\b|\s+)") for pat in data[c][t] if pat.strip()]
                    else:
                        contem[c] = [re.compile(f"{pat}") for pat in data[c][t] if pat.strip()]

            return True
        except Exception as e:
            # Lidar com a exceção, se necessário
            log_verbose(self._verbose, f"Erro ao ler o arquivo {caminho_arquivo}: {e}")
            return False
        finally:
            # Certifique-se de fechar o arquivo, mesmo em caso de exceção
            if f:
                f.close()

    def _carregar_autorias_padroes(self):

        self._show_message("> carregando arquivo de padrões - autoria")

        self._autorias_precisos = {}
        self._autorias_comeca_com={}
        self._autorias_contem={}

        return self._carregar_arquivo_padroes(
            './autorias.json',
            [
                'masculino',
                'feminino',
                'empresa',
                'coletivo',
                'outros'
                ],
            self._autorias_precisos,
            self._autorias_comeca_com,
            self._autorias_contem
            )

    def _carregar_mencoes_padroes(self):

        self._show_message("> carregando arquivo de padrões - menções")

        self._mencoes_padroes_precisos = {}
        self._mencoes_padroes_comeca_com = {}
        self._mencoes_padroes_contem = {}

        return self._carregar_arquivo_padroes(
            './mencoes.json',
            [
                'saloes_humor',
                'hqmix',
                'ccxp',
                'fiq',
                'angelo_agostini',
                'politica',
                'questoes_genero',
                'lgbtqiamais',
                'terror',
                'humor',
                'herois',
                'disputa',
                'ficcao_cientifica',
                'fantasia',
                'folclore',
                'zine',
                'webformatos',
                'erotismo',
                'religiosidade',
                'jogos',
                'midia_independente'
                ],
            self._mencoes_padroes_precisos,
            self._mencoes_padroes_comeca_com,
            self._mencoes_padroes_contem
            )

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

        self._show_message("> carregar arquivos de conversão monetária")

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

        self._show_message("> carregar arquivos de álbuns")

        result = self._carregar_json(CAMINHO_ALBUNS)
        if result['sucesso']:
            self._albuns = result['json']
        return result['sucesso']

    def _carregar_municipios(self):

        self._show_message("> carregar municípios")

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

    def _adaptar_apoiase(self, campanha_apoiase):
        data = {}
        data['detail'] = {}
        data['detail']['user'] = {}
        data['detail']['address'] = {}
        data['rewards'] = []
        data['user'] = {}
        
        data['detail']['online_date'] = campanha_apoiase['createdDate'].replace('Z', '')#
        data['detail']['expires_at'] = campanha_apoiase.get('dueDate', '').replace('Z', '')#
        if len(campanha_apoiase['goals']) > 0:
            data['detail']['goal']  = campanha_apoiase['goals'][0]['value']#
        else:
            data['detail']['goal']  = 0

        data['detail']['about_html'] = campanha_apoiase['about'].get('desc', campanha_apoiase['about'].get('what','') )#
        data['detail']['name'] = campanha_apoiase.get('name', campanha_apoiase['about'].get('slogan', campanha_apoiase['about'].get('what','')))

        for add in campanha_apoiase['complemento']['address']:
            data['detail']['address']['city'] = add['city']#
            data['detail']['address']['state_acronym'] = add.get('state', '')#
            break
        data['detail']['address']['city'] = data['detail']['address'].get('city', '')
        data['detail']['address']['state_acronym'] = data['detail']['address'].get('state_acronym', '')

            
        data['detail']['city_id'] = -1#
        data['detail']['content_rating'] = None#
        data['detail']['contributed_by_friends'] = None#
        data['detail']['cover_image'] = None#
        data['detail']['video_cover_image'] = None#
        data['detail']['online_days'] = calcular_diferenca_dias(data['detail']['online_date'], data['detail']['expires_at'])#

        data['detail']['is_adult_content'] = False#
        data['detail']['posts_count'] = 0#
        data['detail']['project_id'] = campanha_apoiase['_id']#
        data['detail']['mode'] = 'unknown'#

        data['detail']['total_contributions'] = 0
        data['detail']['total_contributors'] = 0
        for camp in campanha_apoiase['complemento']['campaigns']:
            if camp['_id']==campanha_apoiase['_id']:
                data['detail']['posts_count'] = camp['contentCount']#
                data['detail']['total_contributions'] = camp['supports']['total'].get('count', 0)#
                data['detail']['total_contributors'] = camp['supports']['total'].get('count', 0)#
                data['detail']['pledged'] = camp['supports']['total'].get('value', 0)
                if data['detail']['goal'] == 0:#
                    data['detail']['progress'] = 0#
                else:#
                    data['detail']['progress'] = campanha_apoiase['supports']['total'].get('value', campanha_apoiase['supports']['total'].get('total', 0)) / data['detail']['goal']##

                if campanha_apoiase['fundingFrequency'] == 'oneTime':#
                    if campanha_apoiase['fundingModel'] == 'keepWhatYouRaise':#
                        data['detail']['mode'] = 'flex'#
                        if data['detail']['progress'] > 0:#
                            data['detail']['state'] = 'successful'#
                        else:
                            data['detail']['state'] = 'failed'#
                    else:#
                        data['detail']['mode'] = 'aon'#
                        if data['detail']['progress'] >= 100:#
                            data['detail']['state'] = 'successful'#
                        else:#
                            data['detail']['state'] = 'failed'#
                elif campanha_apoiase['fundingFrequency'] == 'recurring':#
                    data['detail']['mode'] = 'sub'#
                    data['detail']['state'] = campanha_apoiase['status']#


                data['user']['id'] = str(uuid.uuid4())
                data['user']['name'] = camp['name']#
                data['user']['public_name'] = camp['name']#
                data['user']['followers_count'] = 0#
                data['user']['newsletter'] = False#
                data['user']['subscribed_to_friends_contributions'] = 0#
                data['user']['subscribed_to_new_followers'] = 0#
                data['user']['subscribed_to_project_posts'] = 0#
                data['user']['total_contributed_projects'] = 0#
                data['user']['total_published_projects'] = 0#
                data['user']['followers_count'] = 0#

                data['detail']['user'] = data['user']#

                for rwd in camp['rewards']:#
                    r = {}#
                    r['minimum_value'] = rwd['value']#
                    data['rewards'].append(r)#
                break

        return data
    
    def _carregar_campanhas_apoiase(self):
        self._show_message('> campanhas apoia.se')
        if not os.path.exists(CAMINHO_CAMPANHAS_APOIASE):
            return False
        
        caminho_campanhas = os.listdir(CAMINHO_CAMPANHAS_APOIASE)

        quantidade_campanhas = 0

        # Percorre a lista de arquivos
        for caminho_campanha in caminho_campanhas:
            # Cria o caminho completo para o file
            full_path = os.path.join(CAMINHO_CAMPANHAS_APOIASE, caminho_campanha)
            
            # Verifica se o caminho é um arquivo
            if os.path.isfile(full_path) and full_path.endswith(".json"):
                # abrir arquivo
                f = open (full_path, "r")
                
                # ler arquivo como json
                data = json.loads(f.read())

                # fechar arquivo
                f.close()

                data = self._adaptar_apoiase(data)
                data[colunaslib.COL_ORIGEM] = 'apoia.se'

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
        log_verbose(self._verbose, f'\tcampanhas encontradas: {quantidade_campanhas}')
        return True

    def _carregar_campanhas_catarse(self):
        self._show_message('> campanhas catarse')
        if not os.path.exists(CAMINHO_CAMPANHAS_CATARSE):
            return False
        
        caminho_campanhas = os.listdir(CAMINHO_CAMPANHAS_CATARSE)

        quantidade_campanhas = 0

        # Percorre a lista de arquivos
        for caminho_campanha in caminho_campanhas:
            # Cria o caminho completo para o file
            full_path = os.path.join(CAMINHO_CAMPANHAS_CATARSE, caminho_campanha)
            
            # Verifica se o caminho é um arquivo
            if os.path.isfile(full_path) and full_path.endswith(".json"):
                # abrir arquivo
                f = open (full_path, "r")
                
                # ler arquivo como json
                data = json.loads(f.read())
                data[colunaslib.COL_ORIGEM] = 'catarse'

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
        log_verbose(self._verbose, f'\tcampanhas encontradas: {quantidade_campanhas}')
        return True
    
    def _garantir_pastas_normalizacao(self):
        self._show_message('Verificando pastas')
        log_verbose(self._verbose, f"> pasta: {CAMINHO_NORMALIZADOS}")
        if not os.path.exists(f"{CAMINHO_NORMALIZADOS}"):
            log_verbose(self._verbose, f"\tcriando pasta: {CAMINHO_NORMALIZADOS}")
            os.mkdir(f"{CAMINHO_NORMALIZADOS}")
        log_verbose(self._verbose, f"> pasta: {CAMINHO_NORMALIZADOS}/{self._ano}")
        if not os.path.exists(f"{CAMINHO_NORMALIZADOS}/{self._ano}"):
            log_verbose(self._verbose, f"\tcriando pasta: {CAMINHO_NORMALIZADOS}/{self._ano}")
            os.mkdir(f"{CAMINHO_NORMALIZADOS}/{self._ano}")

        return True

    # Função de filtro para remover números e palavras no formato \d+x\d+
    def filter_words(self, words):
        return [word for word in words if not re.match(r"^\d+$", word) and not re.match(r"^\d+x\d+$", word)][-5:]

    def _classificar_multirrotulo(self, msg):

        print(msg)

        try:        
            # Baixar as stopwords do NLTK
            nltk.download('stopwords')
            portuguese_stopwords = stopwords.words('portuguese')

            # novas palavras para ignorar na análise
            portuguese_stopwords.append('_blank')
            portuguese_stopwords.append('apoiador')
            portuguese_stopwords.append('apoiadores')
            portuguese_stopwords.append('apoio')
            portuguese_stopwords.append('aqui')
            portuguese_stopwords.append('br')
            portuguese_stopwords.append('campanha')
            portuguese_stopwords.append('capa')
            portuguese_stopwords.append('catarse')
            portuguese_stopwords.append('cm')
            portuguese_stopwords.append('edição')
            portuguese_stopwords.append('editora')
            portuguese_stopwords.append('email')
            portuguese_stopwords.append('entrega')
            portuguese_stopwords.append('entregue')
            portuguese_stopwords.append('exemplar')
            portuguese_stopwords.append('exemplares')
            portuguese_stopwords.append('facebook')
            portuguese_stopwords.append('formato')
            portuguese_stopwords.append('formatos')
            portuguese_stopwords.append('história')
            portuguese_stopwords.append('histórias')
            portuguese_stopwords.append('hq')
            portuguese_stopwords.append('hqs')
            portuguese_stopwords.append('http')
            portuguese_stopwords.append('https')
            portuguese_stopwords.append('href')
            portuguese_stopwords.append('ilustração')
            portuguese_stopwords.append('ilustrações')
            portuguese_stopwords.append('ilustrador')
            portuguese_stopwords.append('ilustradora')
            portuguese_stopwords.append('instagram')
            portuguese_stopwords.append('livro')
            portuguese_stopwords.append('livros')
            portuguese_stopwords.append('meta')
            portuguese_stopwords.append('narrativa')
            portuguese_stopwords.append('narrativas')
            portuguese_stopwords.append('página')
            portuguese_stopwords.append('páginas')
            portuguese_stopwords.append('papel')
            portuguese_stopwords.append('pdf')
            portuguese_stopwords.append('projeto')
            portuguese_stopwords.append('projetos')
            portuguese_stopwords.append('quadrinho')
            portuguese_stopwords.append('quadrinhos')
            portuguese_stopwords.append('quadrinista')
            portuguese_stopwords.append('quadrinistas')
            portuguese_stopwords.append('recompensa')
            portuguese_stopwords.append('recompensas')
            portuguese_stopwords.append('revista')
            portuguese_stopwords.append('revistas')
            portuguese_stopwords.append('roteirista')
            portuguese_stopwords.append('site')
            portuguese_stopwords.append('sobre')
            portuguese_stopwords.append('target')
            portuguese_stopwords.append('toda')
            portuguese_stopwords.append('todas')
            portuguese_stopwords.append('todo')
            portuguese_stopwords.append('todos')
            portuguese_stopwords.append('twitter')
            portuguese_stopwords.append('valor')
            portuguese_stopwords.append('volume')
            portuguese_stopwords.append('x')
            portuguese_stopwords.append('www')            

            texts = [t['detail']['about_txt'] for t in self._campanhas]

            # Vetorização
            #vectorizer = TfidfVectorizer()
            vectorizer = CountVectorizer(stop_words=portuguese_stopwords)
            X = vectorizer.fit_transform(texts)

            # Modelagem de tópicos com LDA
            lda = LatentDirichletAllocation(n_components=50, random_state=42)
            lda.fit(X)

            # Palavras-chave de cada tópico
            feature_names = vectorizer.get_feature_names_out()

            selected_topics = {}

            for i, topic in enumerate(lda.components_):
                words = [feature_names[j] for j in topic.argsort()[-29:] ] 
                filtered_words = self.filter_words(words)  # Aplicar o filtro
                selected_topics[i] = filtered_words
                print('.', end='', flush=True)
            print('')

            arquivo_dados = f"topicos_classificacao.json"
            
            with open(arquivo_dados, 'w') as arquivo_json:
                json.dump(selected_topics, arquivo_json)

            for data in self._campanhas:
                txt = data['detail']['about_txt']
                print('.', end='', flush=True)

                no_topico = True
                # verifica se o texto participa de cada tópico
                for k, tokens in selected_topics.items():
                    cont = 0.0
                    for token in tokens:
                        if self._testar_regex(txt, re.compile(fr'\b{re.escape(token)}\b')):
                            cont = cont + 1.0
    

                    data[f'topico_{k}'] = (cont / len(tokens))

            print('')
            
        except Exception as e:
            # Lidar com a exceção, se necessário
            log_verbose(self._verbose, f"Erro ao classificar multirrotulo: {e}")
            return False

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
        data['detail']['goal_ajustado'] = self._ajustar_valor(data_obj.year, data_obj.month, data['detail']['goal'], self._ano, 12)
        data['detail']['pledged_ajustado'] = self._ajustar_valor(data_obj.year, data_obj.month, data['detail']['pledged'], self._ano, 12)

        # ajustar valores das recompensas
        for reward in data['rewards']:
            reward['minimum_value_ajustado'] = self._ajustar_valor(data_obj.year, data_obj.month, reward['minimum_value'], self._ano, 12)
            #reward['maximum_contributions_ajustado'] = self._ajustar_valor(data_obj.year, data_obj.month, reward['maximum_contributions'], self._ano, 12)
        return True

    def _ajustar_valor_about(self, data):
        # converter texto de about the HTML (com tags) para TEXT (texto puro, sem marcação)
        about_html = data['detail']['about_html']
        soup = BeautifulSoup(about_html, 'html.parser')
        about_txt = soup.get_text(separator=' ', strip=True)
        data['detail']['about_txt'] = about_txt

        return True
    

    def _testar_regex(self, text, pattern):
        if not (pattern.search(text) is None):
            return True
        else:
            return False

    def _classificar_mencoes(self, data):
        about_txt = data['detail']['about_txt']
        if about_txt is None:
            about_txt = ''

        about_txt = about_txt.lower()

        cats = [
            self._mencoes_padroes_precisos,
            self._mencoes_padroes_comeca_com,
            self._mencoes_padroes_contem
            ]
        for c in cats:
            for k, v in c.items():
                for p in v:
                    chave = f'mencoes_{k}'
                    data[chave] = self._testar_regex(about_txt, p)
                    if data[chave]:
                        break

        return True

    def _classificar_recompensas(self, data):
        menor_ajustado = 10000000000
        menor = menor_ajustado
        for reward in data['rewards']:
            valor_ajustado = float(reward['minimum_value_ajustado'])
            if valor_ajustado < menor_ajustado:
                menor_ajustado = valor_ajustado
            valor = float(reward['minimum_value'])
            if valor < menor:
                menor = valor

        data[colunaslib.COL_RECOMPENSAS_MENOR_NOMINAL] = menor
        data[colunaslib.COL_RECOMPENSAS_MENOR_AJUSTADO] = menor_ajustado
        data[colunaslib.COL_RECOMPENSAS_QUANTIDADE] = len(data['rewards'])

        return True

    def _classificar_autoria(self, data):
        user_data = data['user']
        public_name = user_data['public_name']
        name = user_data['name']

        if public_name == "" or public_name is None:
            public_name = name
        if name == "" or name is None:
            name = ''

        public_name = public_name.lower().strip()
        name = name.lower().strip()

        categoria = 'indefinido'
        cats = [
            self._autorias_precisos,
            self._autorias_comeca_com,
            self._autorias_contem
            ]
        for c in cats:
            for k, v in c.items():
                for p in v:
                    if self._testar_regex(public_name, p):
                        categoria = k
                        break
                if categoria != 'indefinido':
                    break
            if categoria != 'indefinido':
                break


        if public_name!='' and categoria=='indefinido':
            primeiro_nome = public_name.split(' ')[0]
            if self._testar_regex(primeiro_nome, REGEX_PRIMEIRO_NOME):
                primeiro_nome = unidecode(primeiro_nome)
                categoria = self._verificar_genero(primeiro_nome)
                if categoria is None:
                    categoria = 'indefinido'
                elif categoria == 'M':
                    categoria = 'masculino'
                else:
                    categoria = 'feminino'

        if categoria=="indefinido":
            categoria = "outros"

        data[colunaslib.COL_AUTORIA_ID] =  data['user']['id']
        data[colunaslib.COL_AUTORIA_NOME] =  name
        data[colunaslib.COL_AUTORIA_NOME_PUBLICO] = public_name
        data[colunaslib.COL_AUTORIA_CLASSIFICACAO] = categoria

        data[colunaslib.COL_SOCIAL_SEGUIDORES] = data['user']['followers_count']
        data[colunaslib.COL_SOCIAL_NEWSLETTER] = data['user']['newsletter']
        data[colunaslib.COL_SOCIAL_SUB_CONTRIBUICOES_AMIGOS] = data['user']['subscribed_to_friends_contributions']
        data[colunaslib.COL_SOCIAL_SUB_NOVOS_SEGUIDORES] = data['user']['subscribed_to_new_followers']
        data[colunaslib.COL_SOCIAL_SUB_POSTS_PROJETO] = data['user']['subscribed_to_project_posts']
        data[colunaslib.COL_SOCIAL_PROJETOS_CONTRIBUIDOS] = data['user']['total_contributed_projects']
        data[colunaslib.COL_SOCIAL_PROJETOS_PUBLICADOS] = data['user']['total_published_projects']
        data[colunaslib.COL_SOCIAL_SEGUIDORES] = data['user']['followers_count']

        return True

    def _somente_uf_brasileira(self, uf):
        if uf in self._uf_brasileiras:
            return uf
        
        return 'XX'
    
    def _classificar_resumo(self, data):

        data[colunaslib.COL_GERAL_MUNICIPIO]=data['detail']['address']['city']
        data[colunaslib.COL_GERAL_UF]=data['detail']['address']['state_acronym']
        data[colunaslib.COL_GERAL_UF_BR] = self._somente_uf_brasileira(data[colunaslib.COL_GERAL_UF])
        data[colunaslib.COL_GERAL_CITY_ID] = data['detail']['city_id']
        data[colunaslib.COL_GERAL_CONTENT_RATING] = data['detail']['content_rating']
        data[colunaslib.COL_GERAL_CONTRIBUTED_BY_FRIENDS] = data['detail']['contributed_by_friends']
        data[colunaslib.COL_GERAL_CAPA_IMAGEM] = not(data['detail']['cover_image'] is None)
        data[colunaslib.COL_GERAL_CAPA_VIDEO] = (data['detail'].get('video_cover_image', None) is not None) or (data['detail'].get('video_embed_url', None) is not None)
        data[colunaslib.COL_GERAL_DIAS_CAMPANHA] = data['detail']['online_days']
        data[colunaslib.COL_GERAL_DATA_FIM] = data['detail']['expires_at']
        data[colunaslib.COL_GERAL_DATA_INI] = data['detail']['online_date']
        data[colunaslib.COL_GERAL_META] = data['detail']['goal']
        data[colunaslib.COL_GERAL_META_CORRIGIDA] = data['detail']['goal_ajustado']
        data[colunaslib.COL_GERAL_ARRECADADO] = data['detail']['pledged']
        data[colunaslib.COL_GERAL_ARRECADADO_CORRIGIDO] = data['detail']['pledged_ajustado']
        data[colunaslib.COL_GERAL_PERCENTUAL_ARRECADADO] = data['detail']['progress']
        data[colunaslib.COL_GERAL_CONTEUDO_ADULTO] = data['detail']['is_adult_content']
        data[colunaslib.COL_GERAL_POSTS] = data['detail']['posts_count']
        data[colunaslib.COL_GERAL_PROJECT_ID] = data['detail']['project_id']
        data[colunaslib.COL_GERAL_MODALIDADE] = data['detail']['mode']
        data[colunaslib.COL_GERAL_TITULO] = data['detail']['name']
        data[colunaslib.COL_GERAL_STATUS] = data['detail']['state']
        data[colunaslib.COL_GERAL_TOTAL_CONTRIBUICOES] = data['detail']['total_contributions']
        data[colunaslib.COL_GERAL_TOTAL_APOIADORES] = data['detail']['total_contributors']

        #if not (data['detail']['user']['id'] in self._autores):
        #    self._autores[data['detail']['user']['id']]={
        #        "name": data['detail']['user']['name'],
        #        "public_name": data['detail']['user']['public_name']
        #    }

        return True

    def _gravar_json_campanhas(self, data):

        try:        
            arquivo_dados = f"{CAMINHO_NORMALIZADOS}/{self._ano}/{data['detail']['project_id']}.json"
            data[colunaslib.COL_GERAL_SOBRE] = data['detail']['about_txt']
            
            del data['detail']
            del data['rewards']
            del data['user']
            
            with open(arquivo_dados, 'w') as arquivo_json:
                json.dump(data, arquivo_json)
        except Exception as e:
            # Lidar com a exceção, se necessário
            log_verbose(self._verbose, f"Erro ao gravar arquivo normalizado {arquivo_dados}: {e}")
            return False
        # finally:
        #     # Certifique-se de fechar o arquivo, mesmo em caso de exceção
        #     if f:
        #         f.close()

        return True
    
    def _show_message(self, msg):
        log_verbose(self._verbose, msg)
        return True

    def executar(self):
        result = True

        self._campanhas = []
        #self._autores = {}

        
        result = (result
            and self._show_message("Carregar arquivos de apoio")
            and self._carregar_uf_brasileiras()
            and self._carregar_arquivos_frequencia_nomes()
            and self._carregar_mencoes_padroes()
            and self._carregar_autorias_padroes()
            and self._carregar_conversao_monetaria()
            and self._carregar_albuns()
            and self._carregar_municipios()

            and self._show_message("Carregar campanhas")
            and self._carregar_campanhas_catarse()
            and self._carregar_campanhas_apoiase()
            and self._garantir_pastas_normalizacao()

            and self._show_message("Normalizar")
            and self._percorrer_campanhas(f'> ajustar valores das campanhas para dez/{self._ano}', self._ajustar_valores_campanha)
            and self._percorrer_campanhas(f'> texto de apresentação: HTML -> Texto', self._ajustar_valor_about)
            and self._percorrer_campanhas(f'> categorizar textos de apresentação', self._classificar_mencoes)
            and self._percorrer_campanhas(f'> categorizar recompensas', self._classificar_recompensas)
            and self._percorrer_campanhas(f'> classificar autoria', self._classificar_autoria)
            and self._percorrer_campanhas(f'> categorizar resumo', self._classificar_resumo)

            and self._classificar_multirrotulo(f'> categorizar multirrotulo')

            and self._percorrer_campanhas(f'> gravar arquivos normalizados das campanhas', self._gravar_json_campanhas)
        )


        colunas = colunaslib.COLUNAS_NORMALIZACAO

        df = pd.DataFrame(self._campanhas, columns=colunas)

        analise_mencoes = [am for am in colunas if 'mencoes_' in am]

        resultados_mencoes = {}
        for m in analise_mencoes:
            parcial = df[df[m] == True]
            resultados_mencoes[m] = len(parcial)
        dfmencoes = pd.DataFrame(list(resultados_mencoes.items()), columns=['Chave', 'Quantidade']).set_index('Chave')
        print(dfmencoes)
        #dfmencoes.to_excel(f'{CAMINHO_CSV}/{self._ano}/mencoes_{self._ano}.xlsx', index=False, columns=['Chave', 'Quantidade'])
        

        #if result:
        #    arquivo_dados = f"{CAMINHO_NORMALIZADOS}/autores_{self._ano}.json"
        #    with open(arquivo_dados, 'w') as arquivo_json:
        #        json.dump(self._autores, arquivo_json)
            



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
    log_filename = f"log/normalizar_{datetime.today().strftime('%Y%m%d_%H%M%S')}.log"

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