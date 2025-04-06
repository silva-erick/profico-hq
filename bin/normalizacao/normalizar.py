import os
import asyncio
import logging
from datetime import datetime, timedelta

import pandas as pd
from unidecode import unidecode

import re
import json
import uuid

from bs4 import BeautifulSoup

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.cluster import KMeans
from nltk.corpus import stopwords
import nltk

import logs

import formatos
import normalizacao.colunas as colunaslib


CAMINHO_NORMALIZADOS = "../dados/normalizados"
CAMINHO_CONVERSAO_MONETARIA = "../dados/brutos/aasp/conversao-monetaria.json"
CAMINHO_ALBUNS = "../dados/brutos/guiadosquadrinhos/totais.json"
CAMINHO_MUNICIPIOS = "../dados/brutos/catarse/cities.json"
CAMINHO_CAMPANHAS_CATARSE = "../dados/brutos/catarse/campanhas"
CAMINHO_CAMPANHAS_APOIASE = "../dados/brutos/apoiase/campanhas"

REGEX_PRIMEIRO_NOME = re.compile(r'^[\w]+$')

uf_brasileiras = [
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

nomes_com_genero = {}
'''
async def carregar_arquivos_frequencia_nomes(args)

carregar arquivos de frequências de nome
'''
async def carregar_arquivos_frequencia_nomes(args):
    logs.verbose(args.verbose, 'thread: carregando dicionário de nomes')

    # referência: https://brasil.io/dataset/genero-nomes/nomes/
    # baixado em 2024-01-13
    df = pd.read_csv('./normalizacao/nomes.csv')

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
            if n not in nomes_com_genero:
                nomes_com_genero[n] = genero
        
        quant = quant + 1
        if ( quant > 1000):
            quant = 0
                
    return True


'''
def carregar_arquivo_padroes(args, caminho_arquivo, cats, precisos, comeca_com, contem)

carregar arquivo JSON de padrões, contendo padrões de:
- preciso
- começa com
- contém
'''
def carregar_arquivo_padroes(args, caminho_arquivo, cats, precisos, comeca_com, contem):
    # abrir arquivo
    try:
        f = None
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
        logs.verboseerror(f"Erro ao ler o arquivo {caminho_arquivo}: {e}")
        return False
    finally:
        # Certifique-se de fechar o arquivo, mesmo em caso de exceção
        if f is not None:
            f.close()

autorias_precisos = {}
autorias_comeca_com={}
autorias_contem={}

'''
async def carregar_autorias_padroes(args)

carregar arquivo JSON de padrões de autorias
'''
async def carregar_autorias_padroes(args):

    logs.verbose(args.verbose, f"thread: carregando arquivo de padrões - autoria")

    return carregar_arquivo_padroes(
        args,
        './normalizacao/autorias.json',
        [
            'masculino',
            'feminino',
            'empresa',
            'coletivo',
            'outros'
            ],
        autorias_precisos,
        autorias_comeca_com,
        autorias_contem
        )

mencoes_padroes_precisos = {}
mencoes_padroes_comeca_com = {}
mencoes_padroes_contem = {}
'''
async def carregar_mencoes_padroes(args)

carregar arquivo JSON de padrões de menções
'''
async def carregar_mencoes_padroes(args):

    logs.verbose(args.verbose, f"thread: carregando arquivo de padrões - menções")

    return carregar_arquivo_padroes(
        args,
        './normalizacao/mencoes.json',
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
        mencoes_padroes_precisos,
        mencoes_padroes_comeca_com,
        mencoes_padroes_contem
        )


'''
def carregar_json(caminho)

carregar arquivo JSON
'''
def carregar_json(args, caminho, holder):
    result = {}
    result['sucesso'] = False
    try:
        f = open(caminho, "r")

        # Reading from file
        temp_data = json.loads(f.read())
        if isinstance(temp_data, dict):
            for key, value in temp_data.items():
                holder[key] = value
        elif isinstance(temp_data, list):
            holder.extend(temp_data)
        else:
            holder = temp_data

        result['json'] = temp_data

        result['sucesso'] = True
    except Exception as e:
        # Lidar com a exceção, se necessário
        logs.verbose(args.verbose, f"Erro ao ler o arquivo: {e}")

    finally:
        # Certifique-se de fechar o arquivo, mesmo em caso de exceção
        if f:
            f.close()

        return result

conversao_monetaria = {}
'''
async def carregar_conversao_monetaria(args)

carregar JSON de conversão monetária
'''
async def carregar_conversao_monetaria(args):

    ano = args.ano

    logs.verbose(args.verbose, "thread: carregar arquivos de conversão monetária")

    result = carregar_json(args, CAMINHO_CONVERSAO_MONETARIA, conversao_monetaria)
    if result['sucesso']:
        # existe data de dezembro do ano selecionado?
        ano = str(ano * 100 + 12)
        if (not ano in conversao_monetaria) or (conversao_monetaria[ano] is None):
            logs.verbose(args.verbose, f"Não existe conversão de valores monetários em dezembro/{ano}")
            result['sucesso'] = False
    return result['sucesso']

albuns = {}
'''
async def carregar_albuns(args):

carregar JSON de álbuns
'''
async def carregar_albuns(args):

    logs.verbose(args.verbose, "thread: carregar arquivos de álbuns")

    result = carregar_json(args, CAMINHO_ALBUNS, albuns)

    return result['sucesso']


municipios = []
'''
async def carregar_municipios(args)

carregar JSON de municípios
'''
async def carregar_municipios(args):

    logs.verbose(args.verbose, "thread: carregar municípios")

    result = carregar_json(args, CAMINHO_MUNICIPIOS, municipios)

    return result['sucesso']

'''
def ajustar_valor(ano_ini, mes_ini, valor_ini, ano_fim, mes_fim)

ajustar valor usando a tabela de conversão monetária
'''
def ajustar_valor(ano_ini, mes_ini, valor_ini, ano_fim, mes_fim):
    anomes_ini = str(ano_ini * 100 + mes_ini)
    anomes_fim = str(ano_fim * 100 + mes_fim)

    if valor_ini is None:
        return valor_ini

    return (valor_ini/conversao_monetaria[anomes_ini]) * conversao_monetaria[anomes_fim]

'''
def adaptar_apoiase(campanha_apoiase)

adaptar campanhas do apoiase
'''
def adaptar_apoiase(campanha_apoiase):
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
    data['detail']['online_days'] = formatos.calcular_diferenca_dias(data['detail']['online_date'], data['detail']['expires_at'])#

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

campanhas_apoiase = []

'''
async def carregar_campanhas_apoiase(args)

carregar campanhas do apoiase
'''
async def carregar_campanhas_apoiase(args):
    logs.verbose(args.verbose, 'thread: campanhas apoia.se')
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

            data = adaptar_apoiase(data)
            data[colunaslib.COL_ORIGEM] = 'apoia.se'

            # verificar a data de lançamento da campanha
            try:
                data_obj = formatos.parse_data(data['detail']['online_date'])
            except ValueError:
                print(f"data original: {data['detail']['online_date']}")
                raise ValueError(f"Formato de data inválido. {data['detail']['online_date']}")

            if data_obj.year <= args.ano:
                campanhas_apoiase.append(data)
            else:
                continue

            quantidade_campanhas = quantidade_campanhas + 1

            if args.verbose and ((quantidade_campanhas % 50) == 0):
                print('.', end='', flush=True)

    print('.')
    logs.verbose(args.verbose, f'\tcampanhas encontradas: {quantidade_campanhas}')
    return True


campanhas_catarse=[]
'''
async def carregar_campanhas_catarse(args)

carregar campanhas do catarse
'''
async def carregar_campanhas_catarse(args):
    logs.verbose(args.verbose, 'thread: campanhas catarse')
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
                data_obj = formatos.parse_data(data['detail']['online_date'])
            except ValueError:
                print(f"data original: {data['detail']['online_date']}")
                raise ValueError(f"Formato de data inválido. {data['detail']['online_date']}")

            if data_obj.year <= args.ano:
                campanhas_catarse.append(data)
            else:
                continue

            quantidade_campanhas = quantidade_campanhas + 1

            if args.verbose and ((quantidade_campanhas % 50) == 0):
                print('.', end='', flush=True)

    if args.verbose:
        print('.')

    logs.verbose(args.verbose, f'\tcampanhas encontradas: {quantidade_campanhas}')
    return True

'''
def garantir_pastas_normalizacao(args)

garantir pastas normalizadas
'''
def garantir_pastas_normalizacao(args):
    logs.verbose(args.verbose, 'Verificando pastas')
    logs.verbose(args.verbose, f"> pasta: {CAMINHO_NORMALIZADOS}")
    if not os.path.exists(f"{CAMINHO_NORMALIZADOS}"):
        logs.verbose(args.verbose, f"\tcriando pasta: {CAMINHO_NORMALIZADOS}")
        os.mkdir(f"{CAMINHO_NORMALIZADOS}")
    logs.verbose(args.verbose, f"> pasta: {CAMINHO_NORMALIZADOS}/{args.ano}")
    if not os.path.exists(f"{CAMINHO_NORMALIZADOS}/{args.ano}"):
        logs.verbose(args.verbose, f"\tcriando pasta: {CAMINHO_NORMALIZADOS}/{args.ano}")
        os.mkdir(f"{CAMINHO_NORMALIZADOS}/{args.ano}")

    return True

campanhas = []

'''
def percorrer_campanhas(args, msg, funcao)

apoio: percorrer campanhas
'''
def percorrer_campanhas(args, msg, funcao):
    logs.verbose(args.verbose, msg)
    quantidade_campanhas = 0
    res = True
    for data in campanhas:

        res = funcao(args, data)
        if not res:
            break

        quantidade_campanhas = quantidade_campanhas + 1

        if args.verbose and ((quantidade_campanhas % 50) == 0):
            print('.', end='', flush=True)

    print('.')
    return res



def ajustar_valores_campanha(args, data):
    # verificar a data de lançamento da campanha
    try:
        data_obj = formatos.parse_data(data['detail']['online_date'])
    except ValueError:
        print(f"data original: {data['detail']['online_date']}")
        raise ValueError(f"Formato de data inválido. {data['detail']['online_date']}")

    # ajustar goal e pledged para valor presente
    data['detail']['goal_ajustado'] = ajustar_valor(data_obj.year, data_obj.month, data['detail']['goal'], args.ano, 12)
    data['detail']['pledged_ajustado'] = ajustar_valor(data_obj.year, data_obj.month, data['detail']['pledged'], args.ano, 12)

    # ajustar valores das recompensas
    for reward in data['rewards']:
        reward['minimum_value_ajustado'] = ajustar_valor(data_obj.year, data_obj.month, reward['minimum_value'], args.ano, 12)
        #reward['maximum_contributions_ajustado'] = ajustar_valor(data_obj.year, data_obj.month, reward['maximum_contributions'], args.ano, 12)
    return True

def ajustar_valor_about(args, data):
    # converter texto de about the HTML (com tags) para TEXT (texto puro, sem marcação)
    about_html = data['detail']['about_html']
    soup = BeautifulSoup(about_html, 'html.parser')
    about_txt = soup.get_text(separator=' ', strip=True)
    data['detail']['about_txt'] = about_txt

    return True

def verificar_genero(nome):
    if nome not in nomes_com_genero:
        return None

    return nomes_com_genero[nome]


def testar_regex(args, text, pattern):
    if not (pattern.search(text) is None):
        return True
    else:
        return False

def classificar_mencoes(args, data):
    about_txt = data['detail']['about_txt']
    if about_txt is None:
        about_txt = ''

    about_txt = about_txt.lower()

    cats = [
        mencoes_padroes_precisos,
        mencoes_padroes_comeca_com,
        mencoes_padroes_contem
        ]
    for c in cats:
        for k, v in c.items():
            for p in v:
                chave = f'mencoes_{k}'
                data[chave] = testar_regex(args, about_txt, p)
                if data[chave]:
                    break

    return True

def classificar_recompensas(args, data):
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

def classificar_autoria(args, data):
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
        autorias_precisos,
        autorias_comeca_com,
        autorias_contem
        ]
    for c in cats:
        for k, v in c.items():
            for p in v:
                if testar_regex(args, public_name, p):
                    categoria = k
                    break
            if categoria != 'indefinido':
                break
        if categoria != 'indefinido':
            break


    if public_name!='' and categoria=='indefinido':
        primeiro_nome = public_name.split(' ')[0]
        if testar_regex(args, primeiro_nome, REGEX_PRIMEIRO_NOME):
            primeiro_nome = unidecode(primeiro_nome)
            categoria = verificar_genero(primeiro_nome)
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

def somente_uf_brasileira(uf):
    if uf in uf_brasileiras:
        return uf
    
    return 'XX'

def classificar_resumo(args, data):

    data[colunaslib.COL_GERAL_MUNICIPIO]=data['detail']['address']['city']
    data[colunaslib.COL_GERAL_UF]=data['detail']['address']['state_acronym']
    data[colunaslib.COL_GERAL_UF_BR] = somente_uf_brasileira(data[colunaslib.COL_GERAL_UF])
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

    return True

def gravar_json_campanhas(args, data):

    try:        
        arquivo_dados = f"{CAMINHO_NORMALIZADOS}/{args.ano}/{data['detail']['project_id']}.json"
        data[colunaslib.COL_GERAL_SOBRE] = data['detail']['about_txt']
        
        del data['detail']
        del data['rewards']
        del data['user']
        
        with open(arquivo_dados, 'w') as arquivo_json:
            json.dump(data, arquivo_json)
    except Exception as e:
        # Lidar com a exceção, se necessário
        logs.verbose(args.verbose, f"Erro ao gravar arquivo normalizado {arquivo_dados}: {e}")
        return False
    # finally:
    #     # Certifique-se de fechar o arquivo, mesmo em caso de exceção
    #     if f:
    #         f.close()

    return True


# Função de filtro para remover números e palavras no formato \d+x\d+
def filter_words(words):
    return [word for word in words if not re.match(r"^\d+$", word) and not re.match(r"^\d+x\d+$", word)][-5:]

def classificar_multirrotulo(args, msg):

    print(msg, flush=True)

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

        texts = [t['detail']['about_txt'] for t in campanhas]

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
            filtered_words = filter_words(words)  # Aplicar o filtro
            selected_topics[i] = filtered_words
            print('.', end='', flush=True)
        print('', flush=True)

        arquivo_dados = f"topicos_classificacao.json"
        
        with open(arquivo_dados, 'w') as arquivo_json:
            json.dump(selected_topics, arquivo_json)

        i = 0
        for data in campanhas:
            i = i+1
            if i >= 50:
                i=0
                print('.', end='', flush=True)

            txt = data['detail']['about_txt']
            no_topico = True
            # verifica se o texto participa de cada tópico
            for k, tokens in selected_topics.items():
                cont = 0.0
                for token in tokens:
                    if testar_regex(args, txt, re.compile(fr'\b{re.escape(token)}\b')):
                        cont = cont + 1.0


                data[f'topico_{k}'] = (cont / len(tokens))

        print('.')
        
    except Exception as e:
        # Lidar com a exceção, se necessário
        logs.verbose(args.verbose, f"Erro ao classificar multirrotulo: {e}")
        return False

    return True



'''
async def executar_normalizacao(args)
-- 
'''
async def executar_normalizacao(args):

    p1 = datetime.now()

    logs.definir_log(args, 'normalizar')

    logs.verbose(args.verbose, 'Início')

    threads = list()

    # threads de carregamento de arquivos de dependência
    threads.append(asyncio.create_task(carregar_arquivos_frequencia_nomes(args)))
    threads.append(asyncio.create_task(carregar_autorias_padroes(args)))
    threads.append(asyncio.create_task(carregar_mencoes_padroes(args)))
    threads.append(asyncio.create_task(carregar_conversao_monetaria(args)))
    threads.append(asyncio.create_task(carregar_albuns(args)))
    threads.append(asyncio.create_task(carregar_municipios(args)))

    logs.verbose(args.verbose,'carregando dados...')
    await asyncio.gather(*threads)

    threads.clear()

    # threads de carregamento de campanhas
    threads.append(asyncio.create_task(carregar_campanhas_catarse(args)))
    threads.append(asyncio.create_task(carregar_campanhas_apoiase(args)))

    logs.verbose(args.verbose,'carregando campanhas...')
    await asyncio.gather(*threads)

    threads.clear()

    # unificar campanhas
    campanhas.clear()
    campanhas.extend(campanhas_apoiase)
    campanhas.extend(campanhas_catarse)
    garantir_pastas_normalizacao(args)

    # normalizar campanhas

    logs.verbose(args.verbose,'normalizar campanhas carregadas...')

    result = True
    result = result and percorrer_campanhas(args, f'> ajustar valores das campanhas para dez/{args.ano}', ajustar_valores_campanha)
    result = result and percorrer_campanhas(args, f'> texto de apresentação: HTML -> Texto', ajustar_valor_about)
    result = result and percorrer_campanhas(args, f'> categorizar textos de apresentação', classificar_mencoes)
    result = result and percorrer_campanhas(args, f'> categorizar recompensas', classificar_recompensas)
    result = result and percorrer_campanhas(args, f'> classificar autoria', classificar_autoria)
    result = result and percorrer_campanhas(args, f'> categorizar resumo', classificar_resumo)
    result = result and classificar_multirrotulo(args, f'> categorizar multirrotulo')
    result = result and percorrer_campanhas(args, f'> gravar arquivos normalizados das campanhas', gravar_json_campanhas)

    p2 = datetime.now()
    delta = p2-p1
    tempo = delta.seconds + delta.microseconds/1000000

    logs.verbose(args.verbose, f'Tempo: {tempo}s')


