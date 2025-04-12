import os
import duckdb
import logs
import json
from datetime import datetime, timedelta
import formatos

import pandas as pd


CAMINHO_SQL = "./bancodados/sql"
CAMINHO_SQL_ANALISES = "./bancodados/sql/03-analises"
CAMINHO_ANALISES = "../dados/analises"
CAMINHO_NORMALIZADOS = "../dados/normalizados"


def ler_arquivo(caminho_arq):
    # abrir arquivo
    f = open (caminho_arq, "r")
    # ler arquivo
    return f.read()


'''
def exportar_dados_brutos(args, con)
'''
def exportar_dados_brutos(args, con, caminho_analises_excel):
    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/00-lista-campanhas.sql')
    res = con.sql(sql)
    df = res.to_df()
    df.to_excel(f'{caminho_analises_excel}/00-lista-campanhas.xlsx', index=False)



'''
async def executar_report(args)
-- 
'''
async def executar_report(args):
    p1 = datetime.now()

    caminho_arq = f"{CAMINHO_NORMALIZADOS}/analises_{args.ano}.db"

    print(f'executar análises (duckdb): {caminho_arq}')

    if os.path.exists(caminho_arq):
        os.remove(caminho_arq) 

    caminho_analises = f"{CAMINHO_ANALISES}/{args.ano}"
    caminho_analises_excel = f"{caminho_analises}/excel"

    if not os.path.exists(caminho_analises):
        os.mkdir(caminho_analises)
    if not os.path.exists(caminho_analises_excel):
        os.mkdir(caminho_analises_excel)

    con = duckdb.connect(f"{caminho_analises}/analises_{args.ano}.db")
    
    exportar_dados_brutos(args, con, caminho_analises_excel)


    p2 = datetime.now()
    delta = p2-p1
    tempo = delta.seconds + delta.microseconds/1000000

    logs.verbose(args.verbose, f'Tempo: {tempo}s')
