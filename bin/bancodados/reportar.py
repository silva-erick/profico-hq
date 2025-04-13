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
def exportar_visao_geral(args, con, caminho_analises_excel)
'''
def exportar_visao_geral(args, con, caminho_analises_excel):
    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/01-a-visao-geral-plataformas.sql')
    res = con.sql(sql)
    dfa = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/01-b-visao-geral-top-qtd-uf.sql')
    res = con.sql(sql)
    dfb = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/01-c-visao-geral-top-qtd-classificacao-autoria.sql')
    res = con.sql(sql)
    dfc = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/01-d-visao-geral-top-qtd-autor.sql')
    res = con.sql(sql)
    dfd = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/01-e-visao-geral-top-qtd-categoria-mencao.sql')
    res = con.sql(sql)
    dfe = res.to_df()

    with pd.ExcelWriter(f'{caminho_analises_excel}/01-visao-geral.xlsx') as writer:  
        dfa.to_excel(writer, sheet_name='plataforma', index=False)
        dfb.to_excel(writer, sheet_name='uf', index=False)
        dfc.to_excel(writer, sheet_name='classificacao_autoria', index=False)
        dfd.to_excel(writer, sheet_name='autoria', index=False)
        dfe.to_excel(writer, sheet_name='categoria_mencao', index=False)


'''
async def executar_report(args)
-- 
'''
async def executar_report(args):
    p1 = datetime.now()

    caminho_analises = f"{CAMINHO_ANALISES}/{args.ano}"
    caminho_analises_excel = f"{caminho_analises}/excel"

    caminho_arq = f"{caminho_analises}/analises_{args.ano}.db"

    print(f'executar análises (duckdb): {caminho_arq}')

    if not os.path.exists(caminho_analises_excel):
        os.mkdir(caminho_analises_excel)

    con = duckdb.connect(caminho_arq)
    
    exportar_dados_brutos(args, con, caminho_analises_excel)
    exportar_visao_geral(args, con, caminho_analises_excel)


    p2 = datetime.now()
    delta = p2-p1
    tempo = delta.seconds + delta.microseconds/1000000

    logs.verbose(args.verbose, f'Tempo: {tempo}s')
