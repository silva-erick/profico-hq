###############################################################################
#
# script: raspar_guiaquadrinhos.py
# execução:
#

###############################################################################
#
# bibliotecas
#

import requests
import logging
#import http.client
import re
import datetime
#import json
import re
import html
import os
import argparse
import json
from datetime import datetime

from bs4 import BeautifulSoup

import apoio



###############################################################################
#
# parâmetros
#
URL_GUIA                = "http://guiadosquadrinhos.com/lancamentos-do-mes/{mes}/{ano}"

RE_ALBUM_TITLE                = re.compile("^(.+)\s+-\s+([^\n]+)$")

RE_TOTAL                = re.compile("Itens:\s+\d+\s+-\s+\d+\s+de\s+(\d+)")

###############################################################################
#
# LancamentosGuiaQuadrinhos: controle de execução de requisição de lançamentos
# no site guiadosquadrinhos.com.
#
class LancamentosGuiaQuadrinhos:
    def __init__(self, verbose = False, log_level = logging.WARNING):
        self._nenhum = None
        self._verbose = verbose
        self._log_level = log_level

    # configurar logging
    def configurar_log(self):
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(self._log_level)
        requests_log.propagate = True

    # obter a url de lançamentos
    def obter_url(self, ano, mes):
        return URL_GUIA.replace('{mes}', str(mes)).replace('{ano}', str(ano))
    
    def obter_lancamentos(self, ano, mes):
        # url correspondente ao ano e ao mes
        url = self.obter_url(ano, mes)

        todos_itens = []

        sessao = requests.Session()
        tempo_total = 0
        numero_chamadas = 0
        media_chamada = 0
        chamada_mais_longa = 0
        sucesso = False

        result = apoio.ResultadoApi(False)

        try:
            if self._verbose:
                print(".", end='', flush=True)

            p1 = datetime.now()
            params = {
            }
            req = requests.Request("GET", url, params=params)
            requisicao_preparada = sessao.prepare_request(req)

            numero_chamadas = numero_chamadas + 1
            response = sessao.send(requisicao_preparada, timeout=90)
            p2 = datetime.now()
            delta = p2-p1
            if delta.microseconds > chamada_mais_longa:
                chamada_mais_longa = delta.seconds * 1000000 + delta.microseconds

            tempo_total = tempo_total + delta.microseconds

            if response.status_code == 200 or response.status_code == 206 or response.status_code == 304:
                soup = BeautifulSoup(response.text, 'html.parser')

                # Encontrar a tabela com a classe 'has-fixed-layout'
                span_numberOfPages2 = soup.find('span', {'id': 'MainContent_lstProfileView_dataPageDisplayNumberOfPages2'}).text

                m = RE_TOTAL.search(span_numberOfPages2)
                if not m is None:
                    obj = {}
                    obj['total'] = m.group(1)
                    obj['ano'] = str(ano)
                    obj['mes']  = str(mes)
                    obj['hash'] = f"{obj['ano']}-{obj['mes']}-{obj['total']}"
                    todos_itens.append(obj)

            else:
                result.add_request_error(response.status_code, response.text)
                if self._verbose:
                    print(f"\nErro de requisição: {response.status_code} - {response.text}")

        except requests.exceptions.RequestException as e:
            result.add_request_error(-1, e)
            if self._verbose:
                print(f"\nExceção de requisição: {e}")

        if numero_chamadas == 0:
            media_chamada = 0
        else:
            media_chamada = tempo_total / numero_chamadas

        result.add_summary(sucesso, obj, 1, tempo_total, media_chamada, chamada_mais_longa)

        return result

###############################################################################
#
# raspar_guiadosquadrinhos: controle de execução de requisição de lançamentos
# no site guiadosquadrinhos.com.
#
def raspar_guiaquadrinhos(verbose):
    if not os.path.exists("../../dados/brutos/guiadosquadrinhos"):
        os.makedirs("../../dados/brutos/guiadosquadrinhos")

    api = LancamentosGuiaQuadrinhos(verbose=verbose, log_level=logging.WARNING)
    api.configurar_log()

    hoje = datetime.today()
    ano = 2011
    mes = 1

    print(f"\n{ano}: ", end='')

    run = True
    try:
        if (os.path.exists(f"../../dados/brutos/guiadosquadrinhos/totais.json")):
            os.remove(f"../../dados/brutos/guiadosquadrinhos/totais.json")

        todos_itens = {}
        while run:
            res = api.obter_lancamentos(ano, mes)
            
            if res.resultado:
                todos_itens[ano * 100 + mes] = res.resultado

            mes = mes + 1
            if mes == 13:
                mes = 1
                ano = ano + 1
                print(f"\n{ano}: ", end='')

            if (ano*100 + mes) > (hoje.year*100+hoje.month):
                run = False

        data_file = f"../../dados/brutos/guiadosquadrinhos/totais.json"
        with open(data_file, 'w') as json_file:
            json.dump(todos_itens, json_file)

    except Exception as e:        
        if verbose:
            print(f'\nErro: um erro aconteceu ao processar uma requisição: {e}')
        
        logging.error(f'Um erro aconteceu ao processar uma requisição: {e}')


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog = "raspar_guiaquadrinhos.py",
        description='Obtém dados de lançamentos do guiadequadrinhos.com')
    parser.add_argument('-v', '--verbose',
                    action='store_true')  # on/off flag
    parser.add_argument('-l', '--loglevel', choices=['DEBUG','INFO','WARNING','ERROR','CRITICAL'])
    
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
    log_filename = f"log/guiaquadrinhos_{datetime.today().strftime('%Y%m%d_%H%M%S')}.log"

    if not os.path.exists("../../dados/brutos"):
        os.makedirs("../../dados/brutos")

    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=log_level,
        filename=log_filename,
        datefmt='%Y-%m-%d %H:%M:%S')
    logging.getLogger().setLevel(log_level)

    raspar_guiaquadrinhos(args.verbose)

            