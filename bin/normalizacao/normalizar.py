import os
import asyncio
import logging
from datetime import datetime, timedelta

import pandas as pd
from unidecode import unidecode

import logs
import raspagem.apoio as apoio
import raspagem.aasp as aasp
import raspagem.guia_dos_quadrinhos as guia
import raspagem.catarse as catarse
import raspagem.apoiase as apoiase


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


async def carregar_arquivos_frequencia_nomes(verbose):
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



'''
async def executar_normalizacao(args)
-- 
'''
async def executar_normalizacao(args):

    p1 = datetime.now()

    logs.definir_log(args, 'normalizar')

    logs.verbose(args.verbose, 'Início')

    threads = list()

    # logs.verbose(args.verbose, 'thread: raspar aasp')

    # threads.append(asyncio.create_task(aasp.raspar_aasp(args)))

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

    # logs.verbose(args.verbose,'raspando dados da web')
    # await asyncio.gather(*threads)

    # p2 = datetime.now()
    # delta = p2-p1
    # tempo = delta.seconds + delta.microseconds/1000000

    # logs.verbose(args.verbose, f'Tempo: {tempo}s')


