import os
import asyncio
import logging
from datetime import datetime, timedelta

import concurrent.futures

import pandas as pd
from unidecode import unidecode

import re
import json
import uuid

from bs4 import BeautifulSoup

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.cluster import KMeans
from nltk.corpus import stopwords
import nltk

import spacy

import numpy as np

import logs

import formatos
import normalizacao.colunas as colunaslib
import normalizacao.caminhos as caminhos
import normalizacao.normalizados_comum as normalizados_comum



'''
def obter_entidades_unicas(lista_entidades)

obter entidades únicas
'''
def obter_entidades_unicas(lista_entidades):
    entidades = {}
    for ent in lista_entidades:
        valores = str(ent).lower().split('\n')
        for v in valores:
            entidades[v] = v
    
    return list(entidades.keys())

REGEX_DATA = re.compile(r'^\d{2}/\d{2}/\d{4}$')
REGEX_HORA = re.compile(r'^\d{2}:\d{2}:\d{2}(\.\d{1,3}){0,1}$')

'''
testar regex
'''
def testar_regex(text, pattern):
    if not (pattern.search(text) is None):
        return True
    else:
        return False

'''
rever POS classificado errado pelo modelo
'''
def regra_revisaoPOS_padrao(sintatica):
    resultado = []
    for sint in sintatica:
        val = sint[0]
        pos = sint[1]

        if pos != 'PUNCT' and val in ["'", '"', '!', '@', '#', '$', '%', '¨', '&', '*', '(', ')', '-', '_', '=', '+', '´', '`', '[', ']', '{', '}', '~', '^', ',', '<', '.', '>', ';', ':', '/', '?', '\\', '|', '', '']:
            pos = 'PUNCT'
        elif pos != 'ADP' and val in ['para', 'entre', 'com', 'de', 'da', 'dos', 'das', 'dum', 'duma', 'duns', 'dumas', 'em', 'no', 'na', 'nos', 'nas', 'num', 'numas']:
            pos = 'ADP'
        elif testar_regex(val, REGEX_DATA):
            pos = 'DATA'
        elif testar_regex(val, REGEX_HORA):
            pos = 'HORA'

        it = (val, pos)
        resultado.append(it)

    return resultado

'''
regra: garantir que o conceito tenha pelo menos um nome
'''
def regra_garantir_NOUN(lista_conceitos):
    conceitos = []
    for c in lista_conceitos:
        if len(c) > 1:
            conceitos.append(c)
        elif c[0][1] == 'NOUN' or c[0][1] == 'PROPN':
            conceitos.append(c)
    return conceitos

'''
remover ADP do início
'''
def remover_ADP_inicio(termos):
    if len(termos) == 1:
        if termos[0][1]=='NOUN' or termos[0][1]=='PROPN':
            resultado = termos
    elif termos[0][1] == 'ADP':
        while len(termos)>0 and termos[0][1] == 'ADP':
            termos.pop(0)
        resultado = termos
    else:
        resultado = termos
    return resultado

'''
remover ADP do fim
'''
def remover_ADP_fim(termos):
    if len(termos) == 1:
        if termos[-1][1]=='NOUN' or termos[-1][1]=='PROPN':
            resultado = termos
        else:
            resultado=[]
    elif len(termos)>0 and termos[-1][1] == 'ADP':
        while len(termos)>0 and termos[-1][1] == 'ADP':
            termos = termos[:-1]
        resultado = termos
    else:
        resultado = termos
    return resultado

'''
regra: garantir que o conceito não comece com ADP
'''
def regra_corrigir_comeca_ADP(lista_conceitos):
    conceitos = []
    for c in lista_conceitos:
        candidato = remover_ADP_inicio(c)
        candidato = remover_ADP_fim(c)
        if len(candidato)>0:
            conceitos.append(candidato)
    return conceitos

'''
extrair conceitos do texto
'''
def extrair_conceitos(nlp, texto):
    paragrafos = texto.split('\n')

    conceitos = []

    for p in paragrafos:
        para = nlp(p)
        sintatica = regra_revisaoPOS_padrao([(token.orth_, token.pos_) for token in para])

        parcial = []
        lista_conceitos = []
        for sint in sintatica:
            if sint[1] in ['NOUN', 'ADP', 'ADJ', 'PROPN', 'NUM']:
                parcial.append(sint)
            elif len(parcial) > 0:
                lista_conceitos.append(parcial)
                parcial = []

        if len(parcial)>0:
            lista_conceitos.append(parcial)

        conceitos_resolvidos = regra_garantir_NOUN(lista_conceitos)
        conceitos_resolvidos = regra_corrigir_comeca_ADP(conceitos_resolvidos)

        for c in conceitos_resolvidos:
            conceitos.append(c)

    resultado = []
    for conceito in conceitos:
        termos = []
        for token in conceito:
            termos.append(token[0])
        resultado.append(' '.join(termos))


    return obter_entidades_unicas(resultado)


'''
def classificar_texto_por_extracao_entidades(args, msg)

classificar texto das campanhas por extração de entidades
'''
def classificar_texto_por_extracao_entidades(args, msg, campanhas):

    logs.verbose(args.verbose, msg)

    try:
        nlp = spacy.load('pt_core_news_md')

        # percorrer campanhas para gravar extração de conceitos
        logs.verbose(args.verbose, 'percorrer campanhas para gravar extração de conceitos')
        i = 0
        for data in campanhas:
            i = i+1
            if i >= 50:
                i=0
                print('.', end='', flush=True)

            txt = data['geral_sobre']

            doc = nlp(txt)
            entidades = obter_entidades_unicas(list(doc.ents))
            conceitos = extrair_conceitos(nlp, txt)

            data["categoria_entidades"] = conceitos

        if args.verbose:
            print('.')

        normalizados_comum.gravar_campanhas(args, campanhas)
        
    except Exception as e:
        # Lidar com a exceção, se necessário
        logs.verbose(args.verbose, f"Erro ao classificar multirrotulo: {e}")
        return False

    return True


# Helper function to unpack arguments and call the target function
def unpack_and_classificar(chunk):
    return classificar_texto_por_extracao_entidades(*chunk)

async def executar_extracao_entidades(args):
    p1 = datetime.now()


    logs.verbose(args.verbose, '> categorizar por extração de entidade')

    logs.verbose(args.verbose, 'carregar campanhas')

    campanhas = normalizados_comum.carregar_campanhas_normalizadas(args)
    arr_campanhas = np.array(campanhas)

    # Get the number of CPU cores
    workers = os.cpu_count()

    chunks = [(args, f'extrair entidades...', list(sublist)) for sublist in np.array_split(arr_campanhas, workers)]

    # Process the chunks in parallel
    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
        result = list(executor.map(unpack_and_classificar, chunks))

    p2 = datetime.now()
    delta = p2-p1
    tempo = delta.seconds + delta.microseconds/1000000

    logs.verbose(args.verbose, f'Tempo: {tempo}s')
