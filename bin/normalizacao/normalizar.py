import os
import asyncio
import logging
from datetime import datetime, timedelta

import pandas as pd
from unidecode import unidecode

import re
import json

import logs

CAMINHO_NORMALIZADOS = "../../dados/normalizados"
CAMINHO_CONVERSAO_MONETARIA = "../../dados/brutos/aasp/conversao-monetaria.json"
CAMINHO_ALBUNS = "../../dados/brutos/guiadosquadrinhos/totais.json"
CAMINHO_MUNICIPIOS = "../../dados/brutos/catarse/cities.json"
CAMINHO_CAMPANHAS_CATARSE = "../../dados/brutos/catarse/campanhas"
CAMINHO_CAMPANHAS_APOIASE = "../../dados/brutos/apoiase/campanhas"

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
async def executar_normalizacao(args)
-- 
'''
async def executar_normalizacao(args):

    p1 = datetime.now()

    logs.definir_log(args, 'normalizar')

    logs.verbose(args.verbose, 'Início')

    threads = list()

    threads.append(asyncio.create_task(carregar_arquivos_frequencia_nomes(args)))
    threads.append(asyncio.create_task(carregar_autorias_padroes(args)))
    threads.append(asyncio.create_task(carregar_mencoes_padroes(args)))

    # hoje = datetime.today()
    # ano = 2011
    # mes = 1
    # while ano <= hoje.year:
    #     logs.verbose(args.verbose, f'thread: raspar guia dos quadrinhos: {ano}')
    #     threads.append(asyncio.create_task(guia.raspar_guiaquadrinhos(args, ano)))
    #     ano = ano + 1

    # logs.verbose(args.verbose,'thread: raspar catarse')
    # threads.append(asyncio.create_task(catarse.raspar_catarse(args)))

    # logs.verbose(args.verbose,'thread: raspar catarse categories')
    # threads.append(asyncio.create_task(catarse.raspar_catarse_categories(args)))

    # logs.verbose(args.verbose,'thread: raspar catarse cities')
    # threads.append(asyncio.create_task(catarse.raspar_catarse_cities(args)))

    # logs.verbose(args.verbose,'thread: raspar apoiase')

    # threads.append(asyncio.create_task(apoiase.raspar_apoiase(args)))

    logs.verbose(args.verbose,'carregando dados...')
    await asyncio.gather(*threads)

    p2 = datetime.now()
    delta = p2-p1
    tempo = delta.seconds + delta.microseconds/1000000

    logs.verbose(args.verbose, f'Tempo: {tempo}s')


