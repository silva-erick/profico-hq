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
filter_words(words)

Função de filtro para remover números e palavras no formato \\d+x\\d+
'''
def filter_words(words):
    return [word for word in words if not re.match(r"^\d+$", word) and not re.match(r"^\d+x\d+$", word)][-5:]

def obter_topicos_selecionados(args, campanhas):
    logs.verbose(args.verbose, 'carregando stopwords padrão e manualmente adicionadas')

    # Baixar as stopwords do NLTK
    nltk.download('stopwords')
    portuguese_stopwords = stopwords.words('portuguese')

    # novas palavras para ignorar na análise
    portuguese_stopwords.append('_blank')
    portuguese_stopwords.append('apoiador')
    portuguese_stopwords.append('apoiadores')
    portuguese_stopwords.append('apoio')
    portuguese_stopwords.append('aqui')
    portuguese_stopwords.append('br')
    portuguese_stopwords.append('campanha')
    portuguese_stopwords.append('capa')
    portuguese_stopwords.append('catarse')
    portuguese_stopwords.append('cm')
    portuguese_stopwords.append('edição')
    portuguese_stopwords.append('editora')
    portuguese_stopwords.append('email')
    portuguese_stopwords.append('entrega')
    portuguese_stopwords.append('entregue')
    portuguese_stopwords.append('exemplar')
    portuguese_stopwords.append('exemplares')
    portuguese_stopwords.append('facebook')
    portuguese_stopwords.append('formato')
    portuguese_stopwords.append('formatos')
    portuguese_stopwords.append('história')
    portuguese_stopwords.append('histórias')
    portuguese_stopwords.append('hq')
    portuguese_stopwords.append('hqs')
    portuguese_stopwords.append('http')
    portuguese_stopwords.append('https')
    portuguese_stopwords.append('href')
    portuguese_stopwords.append('ilustração')
    portuguese_stopwords.append('ilustrações')
    portuguese_stopwords.append('ilustrador')
    portuguese_stopwords.append('ilustradora')
    portuguese_stopwords.append('instagram')
    portuguese_stopwords.append('livro')
    portuguese_stopwords.append('livros')
    portuguese_stopwords.append('meta')
    portuguese_stopwords.append('narrativa')
    portuguese_stopwords.append('narrativas')
    portuguese_stopwords.append('página')
    portuguese_stopwords.append('páginas')
    portuguese_stopwords.append('papel')
    portuguese_stopwords.append('pdf')
    portuguese_stopwords.append('projeto')
    portuguese_stopwords.append('projetos')
    portuguese_stopwords.append('quadrinho')
    portuguese_stopwords.append('quadrinhos')
    portuguese_stopwords.append('quadrinista')
    portuguese_stopwords.append('quadrinistas')
    portuguese_stopwords.append('recompensa')
    portuguese_stopwords.append('recompensas')
    portuguese_stopwords.append('revista')
    portuguese_stopwords.append('revistas')
    portuguese_stopwords.append('roteirista')
    portuguese_stopwords.append('site')
    portuguese_stopwords.append('sobre')
    portuguese_stopwords.append('target')
    portuguese_stopwords.append('toda')
    portuguese_stopwords.append('todas')
    portuguese_stopwords.append('todo')
    portuguese_stopwords.append('todos')
    portuguese_stopwords.append('twitter')
    portuguese_stopwords.append('valor')
    portuguese_stopwords.append('volume')
    portuguese_stopwords.append('x')
    portuguese_stopwords.append('www')            

    logs.verbose(args.verbose, 'construção de categorias usando CountVectorizer + LatentDirichletAllocation')


    # montar um vetor com o texto das campanhas
    texts = [t['geral_sobre'] for t in campanhas]

    # Vetorização
    #vectorizer = TfidfVectorizer()
    vectorizer = CountVectorizer(stop_words=portuguese_stopwords)
    X = vectorizer.fit_transform(texts)

    # Modelagem de tópicos com LDA
    lda = LatentDirichletAllocation(n_components=50, random_state=42)
    lda.fit(X)

    # Palavras-chave de cada tópico
    feature_names = vectorizer.get_feature_names_out()

    selected_topics = {}

    logs.verbose(args.verbose, 'percorrer o resultado da vetorização multi-rótulo')
    for i, topic in enumerate(lda.components_):
        words = [feature_names[j] for j in topic.argsort()[-29:] ] 
        filtered_words = filter_words(words)  # Aplicar o filtro
        selected_topics[i] = filtered_words
        if args.verbose:
            print('.', end='', flush=True)
    if args.verbose:
        print('', flush=True)

    arquivo_dados = f"topicos_classificacao.json"
    
    # gravar arquivo de palavras-chave por tópico
    with open(arquivo_dados, 'w') as arquivo_json:
        json.dump(selected_topics, arquivo_json)

    return selected_topics


'''
def classificar_texto_por_analise_multirrotulo(args, msg)

classificar texto das campanhas por abordagem multi-rótulo (count vectorizer + lda)
'''
def classificar_texto_por_analise_multirrotulo(args, selected_topics, campanhas):

    msg = f'categorizar...'
    logs.verbose(args.verbose, msg)

    try:        
        # percorrer campanhas para gravar pertencimento no tópico
        logs.verbose(args.verbose, 'percorrer campanhas para gravar pertencimento nos tópicos multi-rótulo')
        i = 0
        for data in campanhas:
            if args.verbose:
                i = i+1
                if i >= 50:
                    i=0
                    print('.', end='', flush=True)

            txt = data['geral_sobre']
            no_topico = True

            topicos = {}
            # verifica participação do texto em cada tópico encontrado
            for k, tokens in selected_topics.items():
                cont = 0.0
                for token in tokens:
                    if normalizados_comum.testar_regex(txt, re.compile(fr'\b{re.escape(token)}\b')):
                        cont = cont + 1.0


                #data[f'topico_{k}'] = (cont / len(tokens))
                topicos[k] = (cont / len(tokens))
            data["categoria_multirrotulo_lda"] = topicos

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
    return classificar_texto_por_analise_multirrotulo(*chunk)

async def executar_categorizacao_texto(args):
    p1 = datetime.now()

    logs.verbose(args.verbose, '> categorizar multirrotulo')

    logs.verbose(args.verbose, 'carregar campanhas')
    campanhas = normalizados_comum.carregar_campanhas_normalizadas(args)
    topicos_selecionados = obter_topicos_selecionados(args, campanhas)

    arr_campanhas = np.array(campanhas)

    # Get the number of CPU cores
    workers = os.cpu_count()

    chunks = [(args, topicos_selecionados, list(sublist)) for sublist in np.array_split(arr_campanhas, workers)]

    # Process the chunks in parallel
    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
        result = list(executor.map(unpack_and_classificar, chunks))

    p2 = datetime.now()
    delta = p2-p1
    tempo = delta.seconds + delta.microseconds/1000000

    logs.verbose(args.verbose, f'Tempo: {tempo}s')


    p2 = datetime.now()
    delta = p2-p1
    tempo = delta.seconds + delta.microseconds/1000000

    logs.verbose(args.verbose, f'Tempo: {tempo}s')
