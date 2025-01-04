import raspagem.apoio as apoio
from bs4 import BeautifulSoup
import os
import json

import logs

URL = "https://www.aasp.org.br/produtos-servicos/indices-economicos/indices-judiciais/tabela-pratica-para-calculo-de-atualizacao-monetaria-ipca-e/"

'''
async def raspar_aasp(args)
    args:
    . verbose: true/false
'''
async def raspar_aasp(args):
    verbose = args.verbose
    if args.clear_cache:
        if not os.path.exists("../dados/brutos"):
            os.makedirs("../dados/brutos")
        if not os.path.exists("../dados/brutos/aasp"):
            os.makedirs("../dados/brutos/aasp")

    content = ''
    content = await apoio.fetch(URL)

    soup = BeautifulSoup(content, 'html.parser')

    # Encontrar a tabela com a classe 'has-fixed-layout'
    tabela = soup.find('table')

    # Verificar se a tabela foi encontrada
    if tabela:
        todos_itens = {}

        # Iterar sobre as linhas (tr) da tabela
        for linha in tabela.find_all('tr'):
            # Extrair os textos das células (td) da linha
            celulas = linha.find_all('td')
            
            # Verificar se a linha tem 13 células
            if len(celulas) == 13:
                if args.verbose:
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
        logging.error('tabela não encontrada')
        return {}

    try:
        data_file = f"../dados/brutos/aasp/conversao-monetaria.json"
        with open(data_file, 'w') as json_file:
            json.dump(todos_itens, json_file)
    except Exception as e:
        logs.verboseerror(f'\nErro: um erro aconteceu ao gravar arquivo: {e}', e)
