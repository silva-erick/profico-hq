import os
import asyncio
import logging
from datetime import datetime, timedelta
import aiohttp as aiohttp

async def fetch(url, headers = None, params = None):
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url, params=params) as resp:
                return await resp.read()
    except Exception as e:
        logging.error('Error at %s', 'fetching url', exc_info=e)

def eh_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
    
def eh_float(s):
    try:
        float(s.replace('.', '', 1))
        return True
    except ValueError:
        return False
    
def como_inteiro(val, cultura=''):
    if cultura=='pt-br':
        return como_inteiro(val.replace('.', '').replace(',', '.'))
    
    if eh_int(val):
        return int(val)
    
    return None

def como_numerico(val, cultura=''):
    if cultura=='pt-br':
        return como_numerico(val.replace('.', '').replace(',', '.'))
    
    if eh_float(val):
        return float(val)
    
    return None

def calcular_diferenca_dias(data_inicial_str, data_final_str):
    # Converter as strings em objetos datetime
    data_inicial = datetime.fromisoformat(data_inicial_str.replace('Z', ''))
    
    if data_final_str is None:
        # Se a data final for None, use a data atual
        data_final = datetime.utcnow()
    else:
        data_final = datetime.fromisoformat(data_final_str.replace('Z', ''))
    
    # Calcular a diferença em dias
    diferenca = data_final - data_inicial
    
    # Extrair a parte dos dias da diferença
    diferenca_em_dias = diferenca.days
    
    return diferenca_em_dias

def definir_log(args, comando):

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
    log_filename = f"log/{comando}_{datetime.today().strftime('%Y%m%d_%H%M%S')}.log"

    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=log_level,
        filename=log_filename,
        datefmt='%Y-%m-%d %H:%M:%S')
    logging.getLogger().setLevel(log_level)
    
    
def verbose(verbose, msg):
    logging.debug(msg)
    if verbose:
        print(msg, flush=True)
    
    
def verboseerror(msg, e = None):
    if e is Nothing:
        logging.error(msg)
    else:
        logging.error(msg, exc_info=e)
    print(msg, flush=True)


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