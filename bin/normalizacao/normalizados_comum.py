import normalizacao.caminhos as caminhos
import logs
import os
import asyncio
import aiofiles
import logging
from datetime import datetime, timedelta
import re
import json
import uuid


"""
def testar_regex(text, pattern)

testar regex
"""
def testar_regex(text, pattern):
    if not (pattern.search(text) is None):
        return True
    else:
        return False


"""
def carregar_campanhas_normalizadas(args)
"""
def carregar_campanhas_normalizadas(args):
    campanhas = []
    caminho = f'{caminhos.CAMINHO_NORMALIZADOS}/{args.ano}'
    logs.verbose(args, f'carregar campanhas normalizadas, caminho: {caminho}')

    if not os.path.exists(caminho):
        return False
    
    caminho_campanhas = os.listdir(caminho)

    quantidade_campanhas = 0

    # Percorre a lista de arquivos
    for caminho_campanha in caminho_campanhas:
        # Cria o caminho completo para o file
        full_path = os.path.join(caminho, caminho_campanha)
        
        # Verifica se o caminho é um arquivo
        if os.path.isfile(full_path) and full_path.endswith(".json"):
            # abrir arquivo
            f = open (full_path, "r")
            
            # ler arquivo como json
            data = json.loads(f.read())

            # fechar arquivo
            f.close()

            campanhas.append(data)

    return campanhas

"""
def gravar_campanhas(args, campanhas)

gravar campanhas
"""
def gravar_campanhas(args, campanhas):
    logs.verbose(args, "atualizar campanhas")
    quantidade_campanhas = 0
    res = True
    for data in campanhas:

        try:        
            arquivo_dados = f"{caminhos.CAMINHO_NORMALIZADOS}/{args.ano}/{data['geral_project_id']}.json"
            #data[colunaslib.COL_GERAL_SOBRE] = data['geral_sobre']
            
            with open(arquivo_dados, 'w') as arquivo_json:
                json.dump(data, arquivo_json)

        except Exception as e:
            # Lidar com a exceção, se necessário
            logs.verbose(args, f"Erro ao gravar arquivo normalizado {arquivo_dados}: {e}")

        if not res:
            break

        quantidade_campanhas = quantidade_campanhas + 1

        if args.verbose and ((quantidade_campanhas % 50) == 0):
            print('.', end='', flush=True)

    print('.')
    return res
