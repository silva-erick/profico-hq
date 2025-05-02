import os
import asyncio
import logging
from datetime import datetime, timedelta
import aiohttp as aiohttp

async def fetch(url, headers = None, params = None):
    """
    chamar uma url usando os headers e params informados:
    - headers: http headers
    - params: url parameters
    """
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url, params=params) as resp:
                return await resp.read()
    except Exception as e:
        logging.error('Error at %s', 'fetching url', exc_info=e)

class ResultadoApi:
    def __init__(self, sucesso):
        self.sucesso = sucesso

    def add_summary(self, sucesso, resultado, itens, tempo_total, tempo_medio, chamada_mais_longa):
        self.sucesso = sucesso
        self.resultado = resultado
        self.itens = itens
        self.tempo_total = tempo_total
        self.tempo_medio = tempo_medio
        self.chamada_mais_longa = chamada_mais_longa

    def add_request_error(self, code, msg):
        self.code = code
        self.msg = msg
