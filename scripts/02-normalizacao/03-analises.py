import numpy as np
import colunas as colunaslib
import argparse
import logging
from datetime import datetime, timedelta
import time

import os

import re

import pandas as pd

import analises.pontos_notaveis as notaveis
import analises.temporal as tempr

import analises.analises_comum as comum

import analises.analise_descritiva as andesc


CAMINHO_NORMALIZADOS = "../../dados/normalizados"
CAMINHO_CSV = "../../dados/csv"
CAMINHO_TEMPLATE = f"templates"
CAMINHO_TEMPLATE_DESCRITIVO = f"{CAMINHO_TEMPLATE}/descritivo"
CAMINHO_TEMPLATE_NOTAVEIS   = f"{CAMINHO_TEMPLATE}/notaveis"
CAMINHO_TEMPLATE_TEMPORAL = f"{CAMINHO_TEMPLATE}/temporal"

REGEX_PRIMEIRO_NOME = re.compile('^[\w]+$')

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

"""
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
"""    
class AnaliseCsv:
    def __init__(self, ano, verbose):
        self._ano = ano
        self._verbose = verbose

    def _realizar_analise_pontos_notaveis(self, df):
        print(f'. Pontos notáveis')
        
        processos = [
            {'Unidade Federativa': {'arq': 'notaveis_por_ufbr', 'func': notaveis.gerar_ranking_por_ufbr}},
            {'Gênero': {'arq': 'notaveis_por_genero', 'func': notaveis.gerar_ranking_por_genero}},
            {'Autoria': {'arq': 'notaveis_por_autoria', 'func': notaveis.gerar_ranking_por_autoria}},
        ]

        mapa_titulo = {}
        analise_md = []
        i = 1
        pasta_md = f'{CAMINHO_CSV}/{self._ano}/pontos_notaveis'
        if not os.path.exists(pasta_md):
            os.mkdir(pasta_md)
        pasta_dados = f'{CAMINHO_CSV}/{self._ano}/pontos_notaveis/dados'
        if not os.path.exists(pasta_dados):
            os.mkdir(pasta_dados)
        pasta_graficos = f'{CAMINHO_CSV}/{self._ano}/pontos_notaveis/graficos'
        if not os.path.exists(pasta_graficos):
            os.mkdir(pasta_graficos)
                
        with open(f'pontos-notaveis-outros.template.md', 'r', encoding='utf8') as arq_template_pontos_notaveis_modalidade:
            template_pontos_notaveis_modalidade = arq_template_pontos_notaveis_modalidade.read()
            arq_template_pontos_notaveis_modalidade.close()
                
        with open(f'pontos-notaveis.template.md', 'r', encoding='utf8') as arq_template_pontos_notaveis:
            template_pontos_notaveis = arq_template_pontos_notaveis.read()

        with open(f'{CAMINHO_CSV}/{self._ano}/pontos_notaveis/README.md', 'w', encoding='utf8') as f:
            f.write(f'{template_pontos_notaveis}\n')


            arquivos_gerados = []

            for it in processos:
                for titulo, maeamento_funcao in it.items():
                    funcao_mapeada = maeamento_funcao['func']
                    nome_arquivo = maeamento_funcao['arq']
                    mapa_titulo[nome_arquivo] = titulo
                    
                    caminho = f'./{nome_arquivo}.md'
                    #f.write(f'[{titulo}]({caminho})\n\n')

                    template = (f'{template_pontos_notaveis_modalidade.replace("$(nome_dimensao)", titulo)}')

                    tempo_ini = time.time()
                    res = funcao_mapeada(
                                        arquivos_gerados,
                                        df,
                                        self._ano,
                                        pasta_md,
                                        pasta_dados,
                                        nome_arquivo,
                                        titulo,
                                        template
                                        )
                    
                    tempo_fim = time.time()
                    deltaT = tempo_fim - tempo_ini
                    print(f'\t.{i}: {titulo}: {res} - deltaT: {deltaT:.3f}s')
                    i = i + 1
                    if not res:
                        return False

            for mod in comum.MODALIDADES:
                f.write(f'## {comum.TITULOS_MODALIDADES[mod]}\n\n')
                for ag in arquivos_gerados:
                    if ag['mod'] == mod:
                        f.write(f'[{ag["titulo"]}](./{ag["arquivo"]})\n\n')

        f.close()

        return True

    def _realizar_analise_temporal(self, df):
        print(f'. Análise temporal')
        
        processos = [
            {'Modalidade: Tudo ou Nada': {'mod': 'aon', 'arq': 'serie_por_modalidade_aon', 'func': tempr.gerar_serie_por_modalidade_aon}},
            {'Modalidade: Flex': {'mod': 'flex', 'arq': 'serie_por_modalidade_flex', 'func': tempr.gerar_serie_por_modalidade_flex}},
            {'Modalidade: Recorrente': {'mod': 'sub', 'arq': 'serie_por_modalidade_sub', 'func': tempr.gerar_serie_por_modalidade_sub}},
        ]

        mapa_titulo = {}
        analise_md = []
        i = 1
        pasta_md = f'{CAMINHO_CSV}/{self._ano}/serie_temporal'
        if not os.path.exists(pasta_md):
            os.mkdir(pasta_md)
        pasta_dados = f'{CAMINHO_CSV}/{self._ano}/serie_temporal/dados'
        if not os.path.exists(pasta_dados):
            os.mkdir(pasta_dados)
                
        with open(f'analise-temporal-sub.template.md', 'r', encoding='utf8') as arq_template_serie_temporal_sub:
            template_serie_temporal_sub = arq_template_serie_temporal_sub.read()
            arq_template_serie_temporal_sub.close()
                
        with open(f'analise-temporal-modalidade.template.md', 'r', encoding='utf8') as arq_template_serie_temporal_modalidade:
            template_serie_temporal_modalidade = arq_template_serie_temporal_modalidade.read()
            arq_template_serie_temporal_modalidade.close()
                
        with open(f'analise-temporal-outros.template.md', 'r', encoding='utf8') as arq_template_serie_temporal_outros:
            template_serie_temporal_outros = arq_template_serie_temporal_outros.read()
            arq_template_serie_temporal_outros.close()
                
        with open(f'analise-temporal.template.md', 'r', encoding='utf8') as arq_template_serie_temporal:
            template_serie_temporal = arq_template_serie_temporal.read()

        with open(f'{CAMINHO_CSV}/{self._ano}/serie_temporal/README.md', 'w', encoding='utf8') as f:
            f.write(f'{template_serie_temporal}\n')

            for it in processos:
                for titulo, mapeamento_funcao in it.items():
                    funcao_mapeada = mapeamento_funcao['func']
                    nome_arquivo = mapeamento_funcao['arq']
                    mapa_titulo[nome_arquivo] = titulo
                    
                    caminho = f'./{nome_arquivo}.md'
                    f.write(f'[{titulo}]({caminho})\n\n')

                    if nome_arquivo == 'serie_por_modalidade_sub':
                        template = (f'{template_serie_temporal_sub.replace("$(nome_dimensao)", titulo)}')
                    elif nome_arquivo.startswith('serie_por_modalidade_'):
                        template = (f'{template_serie_temporal_modalidade.replace("$(nome_dimensao)", titulo)}')
                    else:
                        template = (f'{template_serie_temporal_outros.replace("$(nome_dimensao)", titulo)}')

                    tempo_ini = time.time()
                    res = funcao_mapeada(df,
                                        self._ano,
                                        pasta_md,
                                        pasta_dados,
                                        nome_arquivo,
                                        titulo,
                                        template,
                                        analise_md
                                        )
                    
                    tempo_fim = time.time()
                    deltaT = tempo_fim - tempo_ini
                    print(f'\t.{i}: {titulo}: {res} - deltaT: {deltaT:.3f}s')
                    i = i + 1
                    if not res:
                        return False

        f.close()

        return True

    def _analisar_campanhas(self):
        self._show_message('> arquivos individuais')

        pasta_normalizados = f'{CAMINHO_NORMALIZADOS}/{self._ano}'
        if not os.path.exists(pasta_normalizados):
            return False
        
        df = pd.read_csv(f'{CAMINHO_CSV}/{self._ano}/campanhas_{self._ano}.csv', sep=';', decimal=',')

        # Calcular apoio médio
        df[colunaslib.COL_GERAL_APOIO_MEDIO] = np.where(df[colunaslib.COL_GERAL_TOTAL_CONTRIBUICOES] != 0, df[colunaslib.COL_GERAL_ARRECADADO_CORRIGIDO] / df[colunaslib.COL_GERAL_TOTAL_CONTRIBUICOES], 0)

        print(f'campanhas: {len(df)}')

        #resultado = (
        #    self._realizar_analise_descritiva(df)
        #    #and self._realizar_analise_pontos_notaveis(df)
        #    #and self._realizar_analise_temporal(df)
        #)

        descritivo = andesc.CoordenadorAnaliseDescritiva()
        resultado = descritivo.executar(df, self._ano)

        return resultado

    def _garantir_pastas(self):
        self._show_message('Verificando pastas')
        # log_verbose(self._verbose, f"> pasta: {CAMINHO_NORMALIZADOS}")
        # if not os.path.exists(f"{CAMINHO_NORMALIZADOS}"):
        #     return False
        # log_verbose(self._verbose, f"> pasta: {CAMINHO_NORMALIZADOS}/{self._ano}")
        # if not os.path.exists(f"{CAMINHO_NORMALIZADOS}/{self._ano}"):
        #     return False

        # log_verbose(self._verbose, f"> pasta: {CAMINHO_CSV}")
        # if not os.path.exists(f"{CAMINHO_CSV}"):
        #     log_verbose(self._verbose, f"\tcriando pasta: {CAMINHO_CSV}")
        #     os.mkdir(f"{CAMINHO_CSV}")
        # log_verbose(self._verbose, f"> pasta: {CAMINHO_CSV}/{self._ano}")
        # if not os.path.exists(f"{CAMINHO_CSV}/{self._ano}"):
        #     log_verbose(self._verbose, f"\tcriando pasta: {CAMINHO_CSV}/{self._ano}")
        #     os.mkdir(f"{CAMINHO_CSV}/{self._ano}")

        return True
    
    def _show_message(self, msg):
        log_verbose(self._verbose, msg)
        return True

    def executar(self):
        result = True

        self._campanhas = []
        
        result = (result
            and self._show_message("Carregando arquivos campanhas")
            and self._garantir_pastas()
            and self._analisar_campanhas()
        )


if __name__ == "__main__":

    print(f'Início: {datetime.now()}')
    start_time = time.time()

    parser = argparse.ArgumentParser(
        prog = "análises",
        description='Exportar os dados como CSV, XLSX e Gráficos')
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
    log_filename = f"log/analises_{datetime.today().strftime('%Y%m%d_%H%M%S')}.log"

    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=log_level,
        filename=log_filename,
        datefmt='%Y-%m-%d %H:%M:%S')
    logging.getLogger().setLevel(log_level)

    if args.verbose:
        print(f"Processar campanhas até {args.ano}")

    arquivo_csv = AnaliseCsv(args.ano, args.verbose)
    arquivo_csv.executar()

    print(f'Encerramento: {datetime.now()}')
    print("--- %s segundos ---" % (time.time() - start_time))