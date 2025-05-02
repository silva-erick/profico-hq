###############################################################################
#
# script: guia_dos_quadrinhos.py
# execução:
#

###############################################################################
#
# bibliotecas
#

import requests
import logging
import re
import datetime
import re
import html
import os
import json
from datetime import datetime

from bs4 import BeautifulSoup

import logs
import raspagem.apoio as apoio



###############################################################################
#
# parâmetros
#
URL_GUIA                = "http://guiadosquadrinhos.com/lancamentos-do-mes/{mes}/{ano}"

RE_ALBUM_TITLE                = re.compile(r"^(.+)\s+-\s+([^\n]+)$")

RE_TOTAL                = re.compile(r"Itens:\s+\d+\s+-\s+\d+\s+de\s+(\d+)")

async def raspar_guiaquadrinhos(args, ano):
    """
    raspar_guiadosquadrinhos: controle de execução de requisição de lançamentos
    no site guiadosquadrinhos.com.
    """

    log_level = args.loglevel
    verbose = args.verbose

    if not os.path.exists("../dados/brutos"):
        os.makedirs("../dados/brutos")

    if not os.path.exists("../dados/brutos/guiadosquadrinhos"):
        os.makedirs("../dados/brutos/guiadosquadrinhos")

    hoje = datetime.today()
    mes = 1

    run = True
    make_download = True
    try:
        
        if (os.path.exists(f"../dados/brutos/guiadosquadrinhos/ano-{ano}.json")):
            if args.clear_cache:
                os.remove(f"../dados/brutos/guiadosquadrinhos/ano-{ano}.json")
            else:
                make_download = False

        if make_download:
            todos_itens = {}
            while run:
                content = await apoio.fetch(URL_GUIA.replace('{mes}', str(mes)).replace('{ano}', str(ano)))

                if content != '':
                    soup = BeautifulSoup(content, 'html.parser')

                    # Encontrar a tabela com a classe 'has-fixed-layout'
                    span_numberOfPages2 = soup.find('span', {'id': 'MainContent_lstProfileView_dataPageDisplayNumberOfPages2'}).text

                    m = RE_TOTAL.search(span_numberOfPages2)
                    if not m is None:
                        obj = {}
                        obj['total'] = m.group(1)
                        obj['ano'] = str(ano)
                        obj['mes']  = str(mes)
                        obj['hash'] = f"{obj['ano']}-{obj['mes']}-{obj['total']}"
                        todos_itens[ano * 100 + mes] = obj

                mes = mes + 1
                if mes == 13:
                    run = False
                elif (ano*100 + mes) > (hoje.year*100+hoje.month):
                    run = False

    except Exception as e:
        logs.verbose_error(f'Erro: um erro aconteceu ao processar uma requisição: {e}')

    try:
        if make_download:
            data_file = f"../dados/brutos/guiadosquadrinhos/ano-{ano}.json"
            with open(data_file, 'w') as json_file:
                json.dump(todos_itens, json_file)
    except Exception as e:
        logs.verbose_error(f'Erro: um erro aconteceu ao gravar arquivo: {e}', e)
