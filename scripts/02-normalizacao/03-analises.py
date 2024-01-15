import argparse
import logging
from datetime import datetime, timedelta
import os
import json

import re

import pandas as pd

import analises.sinteticos as sint

#import csv

CAMINHO_NORMALIZADOS = "../../dados/normalizados"
CAMINHO_CSV = "../../dados/csv"

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
    
class ExportarCsv:
    def __init__(self, ano, verbose):
        self._ano = ano
        self._verbose = verbose

    def _analisar_campanhas(self):
        self._show_message('> arquivos individuais')

        pasta_normalizados = f'{CAMINHO_NORMALIZADOS}/{self._ano}'
        if not os.path.exists(pasta_normalizados):
            return False
        
        colunas = [
            'origem',

            'geral_project_id',
            'geral_titulo',
            'geral_data_ini',
            'geral_data_fim',
            'geral_dias_campanha',
            'geral_percentual_arrecadado',
            'geral_meta',
            'geral_meta_corrigida',
            'geral_arrecadado',
            'geral_arrecadado_corrigido',
            'geral_modalidade',
            'geral_status',
            'geral_uf_br',
            'geral_uf',
            'geral_municipio',
            'geral_city_id',
            'geral_capa_imagem',
            'geral_capa_video',
            'geral_content_rating',
            'geral_conteudo_adulto',
            'geral_contributed_by_friends',
            'geral_posts',
            'geral_total_apoiadores',
            'geral_total_contribuicoes',

            'autoria_classificacao',
            'autoria_nome',
            'autoria_nome_publico',

            'recompensas_menor_nominal',
            'recompensas_menor_ajustado',
            'recompensas_quantidade',

            'social_newsletter',
            'social_projetos_contribuidos',
            'social_projetos_publicados',
            'social_seguidores',

            'mencoes_angelo_agostini',
            'mencoes_ccxp',
            'mencoes_disputa',
            'mencoes_erotismo',
            'mencoes_fantasia',
            'mencoes_ficcao_cientifica',
            'mencoes_fiq',
            'mencoes_folclore',
            'mencoes_herois',
            'mencoes_hqmix',
            'mencoes_humor',
            'mencoes_jogos',
            'mencoes_lgbtqiamais',
            'mencoes_midia_independente',
            'mencoes_politica',
            'mencoes_questoes_genero',
            'mencoes_religiosidade',
            'mencoes_saloes_humor',
            'mencoes_terror',
            'mencoes_webformatos',
            'mencoes_zine',
            
        ]

        df = pd.read_csv(f'{CAMINHO_CSV}/{self._ano}/campanhas_{self._ano}.csv', sep=';', decimal=',')

        print(f'campanhas: {len(df)}')

        #self._sintetico_modalidade(df)
        processos = [
            {'sint_qtd_por_modalidade': sint.calcular_qtd_por_modalidade},
            {'sint_txsucesso_por_modalidade': sint.calcular_txsucesso_por_modalidade},
            {'sint_qtd_por_origem_modalidade': sint.calcular_qtd_por_origem_modalidade},
            {'sint_txsucesso_por_origem_modalidade': sint.calcular_txsucesso_por_origem_modalidade},
            {'sint_qtd_por_ufbr': sint.calcular_qtd_por_ufbr},
            {'sint_txsucesso_por_ufbr': sint.calcular_txsucesso_por_ufbr},

            {'sint_qtd_por_genero': sint.calcular_qtd_por_genero},
            {'sint_txsucesso_por_genero': sint.calcular_txsucesso_por_genero},

            {'sint_qtd_por_mencoes': sint.calcular_qtd_por_mencoes},
            {'sint_txsucesso_por_mencoes': sint.calcular_txsucesso_por_mencoes},
        ]

        i = 1
        for it in processos:
            for k,v in it.items():
                pasta = f'{CAMINHO_CSV}/{self._ano}/{i}'
                if not os.path.exists(pasta):
                    os.mkdir(pasta)
                res = v(df, self._ano, pasta, k)
                print(f'\t.{i}: {k}: {res}')
                i = i + 1
                if not res:
                    return False

        return True
    
    


    def _garantir_pastas(self):
        self._show_message('Verificando pastas')
        log_verbose(self._verbose, f"> pasta: {CAMINHO_NORMALIZADOS}")
        if not os.path.exists(f"{CAMINHO_NORMALIZADOS}"):
            return False
        log_verbose(self._verbose, f"> pasta: {CAMINHO_NORMALIZADOS}/{self._ano}")
        if not os.path.exists(f"{CAMINHO_NORMALIZADOS}/{self._ano}"):
            return False

        log_verbose(self._verbose, f"> pasta: {CAMINHO_CSV}")
        if not os.path.exists(f"{CAMINHO_CSV}"):
            log_verbose(self._verbose, f"\tcriando pasta: {CAMINHO_CSV}")
            os.mkdir(f"{CAMINHO_CSV}")
        log_verbose(self._verbose, f"> pasta: {CAMINHO_CSV}/{self._ano}")
        if not os.path.exists(f"{CAMINHO_CSV}/{self._ano}"):
            log_verbose(self._verbose, f"\tcriando pasta: {CAMINHO_CSV}/{self._ano}")
            os.mkdir(f"{CAMINHO_CSV}/{self._ano}")

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

    arquivo_csv = ExportarCsv(args.ano, args.verbose)
    arquivo_csv.executar()