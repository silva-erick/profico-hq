###############################################################################
#
# script: raspar_aasp.py
# execução:
#

###############################################################################
#
# bibliotecas
#

import requests
import logging
#import http.client
#import re
import datetime
#import json
import re
#import html
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
URL = "https://www.aasp.org.br/suporte-profissional/indices-economicos/indices-judiciais/tabela-pratica-para-calculo-de-atualizacao-monetaria-ipca-e/"


###############################################################################
#
# TabelaConversaoAasp: obter tabela de conversão de valores monetários da AASP
#
class TabelaConversaoAasp:
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
    def obter_url(self):
        return URL
    
    def obter_tabela(self):

        # url correspondente ao ano e ao mes
        url = self.obter_url()

        todos_itens = {}

        sessao = requests.Session()
        tempo_total = 0
        numero_chamadas = 0
        media_chamada = 0
        chamada_mais_longa = 0
        sucesso = False

        result = apoio.ResultadoApi(False)

        try:
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
                tabela = soup.find('table')

                # Verificar se a tabela foi encontrada
                if tabela:
                    # Iterar sobre as linhas (tr) da tabela
                    for linha in tabela.find_all('tr'):
                        # Extrair os textos das células (td) da linha
                        celulas = linha.find_all('td')
                        
                        # Verificar se a linha tem 13 células
                        if len(celulas) == 13:
                            if self._verbose:
                                obj = {
                                    "ano": celulas[0].text,
                                    "jan": celulas[1].text,
                                    "fev": celulas[2].text,
                                    "mar": celulas[3].text,
                                    "abr": celulas[4].text,
                                    "mai": celulas[5].text,
                                    "jun": celulas[6].text,
                                    "jul": celulas[7].text,
                                    "ago": celulas[8].text,
                                    "set": celulas[9].text,
                                    "out": celulas[10].text,
                                    "nov": celulas[11].text,
                                    "dez": celulas[12].text,
                                }
                                print(f'registro: {obj}')
                            # Extrair os valores individuais
                            ano = apoio.como_inteiro(celulas[0].text, 'pt-br')
                            # janeiro
                            todos_itens[ano*100 + 1] = apoio.como_numerico(celulas[1].text, 'pt-br')
                            # fevereiro
                            todos_itens[ano*100 + 2] = apoio.como_numerico(celulas[2].text, 'pt-br')
                            # março
                            todos_itens[ano*100 + 3] = apoio.como_numerico(celulas[3].text, 'pt-br')
                            # abril
                            todos_itens[ano*100 + 4] = apoio.como_numerico(celulas[4].text, 'pt-br')
                            # maio
                            todos_itens[ano*100 + 5] = apoio.como_numerico(celulas[5].text, 'pt-br')
                            # junho
                            todos_itens[ano*100 + 6] = apoio.como_numerico(celulas[6].text, 'pt-br')
                            # julho
                            todos_itens[ano*100 + 7] = apoio.como_numerico(celulas[7].text, 'pt-br')
                            # agosto
                            todos_itens[ano*100 + 8] = apoio.como_numerico(celulas[8].text, 'pt-br')
                            # setembro
                            todos_itens[ano*100 + 9] = apoio.como_numerico(celulas[9].text, 'pt-br')
                            # outubro
                            todos_itens[ano*100 + 10] = apoio.como_numerico(celulas[10].text, 'pt-br')
                            # novembro
                            todos_itens[ano*100 + 11] = apoio.como_numerico(celulas[11].text, 'pt-br')
                            # dezembro
                            todos_itens[ano*100 + 12] = apoio.como_numerico(celulas[12].text, 'pt-br')

                # Se a tabela não for encontrada
                else:
                    print("Tabela não encontrada.")


            else:
                result.add_request_error(response.status_code, response.text)
                if self._verbose:
                    print("")
                    print(f"Erro de requisição: {response.status_code} - {response.text}")

        except requests.exceptions.RequestException as e:
            result.add_request_error(-1, e)
            if self._verbose:
                print("")
                print(f"Exceção de requisição: {e}")

        if numero_chamadas == 0:
            media_chamada = 0
        else:
            media_chamada = tempo_total / numero_chamadas

        result.add_summary(sucesso, todos_itens, len(todos_itens), tempo_total, media_chamada, chamada_mais_longa)

        return result

###############################################################################
#
# raspar_guiadosquadrinhos: controle de execução de requisição de lançamentos
# no site guiadosquadrinhos.com.
#
def raspar_aasp(verbose):
    if not os.path.exists("../../dados/brutos/aasp"):
        os.makedirs("../../dados/brutos/aasp")

    api = TabelaConversaoAasp(log_level=logging.WARNING, verbose=True)
    api.configurar_log()

    try:
        if (os.path.exists(f"../../dados/brutos/aasp/conversao-monetaria.json")):
            os.remove(f"../../dados/brutos/aasp/conversao-monetaria.json")

        res = api.obter_tabela()

        arquivo_dados = f"../../dados/brutos/aasp/conversao-monetaria.json"
        with open(arquivo_dados, 'w') as arquivo_json:
            json.dump(res.resultado, arquivo_json)

    except Exception as e:        
        if verbose:
            print(f'\nErro: um erro aconteceu ao processar uma requisição: {e}')
        
        logging.error(f'Um erro aconteceu ao processar uma requisição: {e}')



if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog = "raspar_aasp.py",
        description='Obtém dados de conversão monetária usando a tabela da AASP')
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
    log_filename = f"log/aasp_{datetime.today().strftime('%Y%m%d_%H%M%S')}.log"

    if not os.path.exists("../../dados/brutos"):
        os.makedirs("../../dados/brutos")

    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=log_level,
        filename=log_filename,
        datefmt='%Y-%m-%d %H:%M:%S')
    logging.getLogger().setLevel(log_level)

    raspar_aasp(args.verbose)

            