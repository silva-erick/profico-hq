import colunas as colunaslib
import argparse
import logging
from datetime import datetime, timedelta
import os
import json

import re

import pandas as pd

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

    def _carregar_campanhas(self):
        self._show_message('> arquivos individuais')

        pasta_normalizados = f'{CAMINHO_NORMALIZADOS}/{self._ano}'
        if not os.path.exists(pasta_normalizados):
            return False
        
        caminho_campanhas = os.listdir(pasta_normalizados)

        quantidade_campanhas = 0

        colunas = colunaslib.COLUNAS_EXPORTACAOCSV

        campanhas = []
        # Percorre a lista de arquivos
        for caminho_campanha in caminho_campanhas:
            # Cria o caminho completo para o file
            full_path = os.path.join(pasta_normalizados, caminho_campanha)

            # Verifica se o caminho é um arquivo
            if not os.path.isfile(full_path):
                continue
            # Verifica se o caminho é um arquivo
            if not full_path.endswith(".json"):
                continue
            
            # abrir arquivo
            f = open (full_path, "r")
            
            # ler arquivo como json
            data = json.loads(f.read())

            # fechar arquivo
            f.close()

            # verificar a data de lançamento da campanha
            try:
                data_obj = parse_data(data[colunaslib.COL_GERAL_DATA_INI])
            except ValueError:
                print(f"data original: {data[colunaslib.COL_GERAL_DATA_INI]}")
                raise ValueError(f"Formato de data inválido. {data[colunaslib.COL_GERAL_DATA_INI]}")

            if data_obj.year > self._ano:
                continue

            data['ano'] = data_obj.year
            campanhas.append(data)

            quantidade_campanhas = quantidade_campanhas + 1

            if self._verbose and ((quantidade_campanhas % 25) == 0):
                print('.', end='', flush=True)

        print('.')
        log_verbose(self._verbose, f'\tcampanhas encontradas: {quantidade_campanhas}')

        df = pd.DataFrame(campanhas, columns=colunas)

        log_verbose(self._verbose, f'exportar csv: {CAMINHO_CSV}/{self._ano}/campanhas_{self._ano}.csv')
        df.to_csv(f'{CAMINHO_CSV}/{self._ano}/campanhas_{self._ano}.csv', index=False, columns=colunas, sep=';', decimal=',', encoding='utf-8-sig')
        log_verbose(self._verbose, f'exportar xlsx: {CAMINHO_CSV}/{self._ano}/campanhas_{self._ano}.xlsx')
        df.to_excel(f'{CAMINHO_CSV}/{self._ano}/campanhas_{self._ano}.xlsx', index=False, columns=colunas)
        
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
            and self._carregar_campanhas()
        )
            



if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog = "exportar-csv",
        description='Exportar os dados como CSV e XLSX')
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
    log_filename = f"log/exportar_csv_{datetime.today().strftime('%Y%m%d_%H%M%S')}.log"

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