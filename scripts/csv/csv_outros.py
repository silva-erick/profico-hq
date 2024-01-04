import argparse
import logging
from datetime import datetime
import os
import json

from bs4 import BeautifulSoup


CAMINHO_NORMALIZADOS = "../../dados/csv"
CAMINHO_CAMPANHAS = "../../dados/brutos/catarse"

def log_verbose(verbose, msg):
    if verbose:
        print(msg)
    logging.debug(msg)

def json_to_csv(origem, destino):
    try:
        f = open(origem, "r")
        g = open(destino, "w", encoding='utf8')

        colunas = [
            'project_id',
            'mode',
            'project_name',
            'online_date',
            'expires_at',
            'owner_name',
            'owner_public_name',
            'city_name',
            'state_acronym',
            'permalink',
            'pledged',
            'progress',
            'state',
            'state_order'
        ]

        # Reading from file
        json_content = json.loads(f.read())
        line = ''
        #data = ''
        first = True
        for c in colunas:
            if not first:
                line = line + ';'
            first = False
            line = line + c
        line = line + '\n'
        g.write(line)

        #data = line

        for reg in json_content:
            first = True
            line = ''
            for c in colunas:
                if not first:
                    line = line + ';'
                first = False

                if c == 'pledged' or c == 'progress':
                    line = line + str(reg[c]).replace('.', ',')
                else:
                    line = line + str(reg[c])
            line = line + '\n'
            #data = data + line
            g.write(line)
        
        g.flush()

    except Exception as e:
        # Lidar com a exceção, se necessário
        print(f"Erro ao ler o arquivo: {e}")
        logging.debug(f"Erro ao ler o arquivo: {e}")

    finally:
        # Certifique-se de fechar o arquivo, mesmo em caso de exceção
        if f:
            f.close()
        if g:
            g.close()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog = "csv_outros.py",
        description='gerar csv a partir dos arquivos finished')
    parser.add_argument('-v', '--verbose',
                    action='store_true')  # on/off flag
    parser.add_argument('-l', '--loglevel', choices=['DEBUG','INFO','WARNING','ERROR','CRITICAL'], required=False)
    
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
    log_filename = f"log/csv_outros_{datetime.today().strftime('%Y%m%d_%H%M%S')}.log"

    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=log_level,
        filename=log_filename,
        datefmt='%Y-%m-%d %H:%M:%S')
    logging.getLogger().setLevel(log_level)

    json_to_csv(f'{CAMINHO_CAMPANHAS}/finished_esporte.json', f'{CAMINHO_NORMALIZADOS}/esporte.csv')
    json_to_csv(f'{CAMINHO_CAMPANHAS}/finished_jornalismo.json', f'{CAMINHO_NORMALIZADOS}/jornalismo.csv')
