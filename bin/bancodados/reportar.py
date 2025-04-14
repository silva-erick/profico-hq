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

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/01-b-visao-geral-uf.sql')
    res = con.sql(sql)
    dfb = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/01-c-visao-geral-classificacao-autoria.sql')
    res = con.sql(sql)
    dfc = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/01-d-visao-geral-autor.sql')
    res = con.sql(sql)
    dfd = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/01-e-visao-geral-categoria-mencao.sql')
    res = con.sql(sql)
    dfe = res.to_df()

    with pd.ExcelWriter(f'{caminho_analises_excel}/01-visao-geral.xlsx') as writer:  
        dfa.to_excel(writer, sheet_name='plataforma', index=False)
        dfb.to_excel(writer, sheet_name='uf', index=False)
        dfc.to_excel(writer, sheet_name='classificacao_autoria', index=False)
        dfd.to_excel(writer, sheet_name='autoria', index=False)
        dfe.to_excel(writer, sheet_name='categoria_mencao', index=False)

'''
def exportar_ranking_tdn_uf(args, con, caminho_analises_excel)
'''
def exportar_ranking_tdn_uf(args, con, caminho_analises_excel):
    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/02-a-ranking-tdn-uf-qtd.sql')
    res = con.sql(sql)
    dfa = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/02-b-ranking-tdn-uf-tot-arrecad.sql')
    res = con.sql(sql)
    dfb = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/02-c-ranking-tdn-uf-avg-arrecad.sql')
    res = con.sql(sql)
    dfc = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/02-d-ranking-tdn-uf-max-arrecad.sql')
    res = con.sql(sql)
    dfd = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/02-e-ranking-tdn-uf-tx-sucesso.sql')
    res = con.sql(sql)
    dfe = res.to_df()

    with pd.ExcelWriter(f'{caminho_analises_excel}/02-ranking-uf-tdn.xlsx') as writer:  
        dfa.to_excel(writer, sheet_name='uf-qtd', index=False)
        dfb.to_excel(writer, sheet_name='uf-tot-arrecad', index=False)
        dfc.to_excel(writer, sheet_name='uf-avg-arrecad', index=False)
        dfd.to_excel(writer, sheet_name='uf-max-arrecad', index=False)
        dfe.to_excel(writer, sheet_name='uf-tx-sucesso', index=False)

'''
def exportar_ranking_tdn_classificacao_autoria(args, con, caminho_analises_excel)
'''
def exportar_ranking_tdn_classificacao_autoria(args, con, caminho_analises_excel):
    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/02-f-ranking-tdn-classificacao-autoria-qtd.sql')
    res = con.sql(sql)
    dfa = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/02-g-ranking-tdn-classificacao-autoria-tot-arrecad.sql')
    res = con.sql(sql)
    dfb = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/02-h-ranking-tdn-classificacao-autoria-avg-arrecad.sql')
    res = con.sql(sql)
    dfc = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/02-i-ranking-tdn-classificacao-autoria-max-arrecad.sql')
    res = con.sql(sql)
    dfd = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/02-j-ranking-tdn-classificacao-autoria-tx-sucesso.sql')
    res = con.sql(sql)
    dfe = res.to_df()

    with pd.ExcelWriter(f'{caminho_analises_excel}/02-ranking-classificacao-autoria-tdn.xlsx') as writer:  
        dfa.to_excel(writer, sheet_name='uf-qtd', index=False)
        dfb.to_excel(writer, sheet_name='uf-tot-arrecad', index=False)
        dfc.to_excel(writer, sheet_name='uf-avg-arrecad', index=False)
        dfd.to_excel(writer, sheet_name='uf-max-arrecad', index=False)
        dfe.to_excel(writer, sheet_name='uf-tx-sucesso', index=False)

'''
def exportar_ranking_tdn_autor(args, con, caminho_analises_excel)
'''
def exportar_ranking_tdn_autor(args, con, caminho_analises_excel):
    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/02-k-ranking-tdn-autor-qtd.sql')
    res = con.sql(sql)
    dfa = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/02-l-ranking-tdn-autor-tot-arrecad.sql')
    res = con.sql(sql)
    dfb = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/02-m-ranking-tdn-autor-avg-arrecad.sql')
    res = con.sql(sql)
    dfc = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/02-n-ranking-tdn-autor-max-arrecad.sql')
    res = con.sql(sql)
    dfd = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/02-o-ranking-tdn-autor-tx-sucesso.sql')
    res = con.sql(sql)
    dfe = res.to_df()

    with pd.ExcelWriter(f'{caminho_analises_excel}/02-ranking-autor-tdn.xlsx') as writer:  
        dfa.to_excel(writer, sheet_name='uf-qtd', index=False)
        dfb.to_excel(writer, sheet_name='uf-tot-arrecad', index=False)
        dfc.to_excel(writer, sheet_name='uf-avg-arrecad', index=False)
        dfd.to_excel(writer, sheet_name='uf-max-arrecad', index=False)
        dfe.to_excel(writer, sheet_name='uf-tx-sucesso', index=False)

'''
def exportar_ranking_tdn_categoria_mencao(args, con, caminho_analises_excel)
'''
def exportar_ranking_tdn_categoria_mencao(args, con, caminho_analises_excel):
    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/02-p-ranking-tdn-categoria-mencao-qtd.sql')
    res = con.sql(sql)
    dfa = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/02-q-ranking-tdn-categoria-mencao-tot-arrecad.sql')
    res = con.sql(sql)
    dfb = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/02-r-ranking-tdn-categoria-mencao-avg-arrecad.sql')
    res = con.sql(sql)
    dfc = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/02-s-ranking-tdn-categoria-mencao-max-arrecad.sql')
    res = con.sql(sql)
    dfd = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/02-t-ranking-tdn-categoria-mencao-tx-sucesso.sql')
    res = con.sql(sql)
    dfe = res.to_df()

    with pd.ExcelWriter(f'{caminho_analises_excel}/02-ranking-categoria-mencao-tdn.xlsx') as writer:  
        dfa.to_excel(writer, sheet_name='uf-qtd', index=False)
        dfb.to_excel(writer, sheet_name='uf-tot-arrecad', index=False)
        dfc.to_excel(writer, sheet_name='uf-avg-arrecad', index=False)
        dfd.to_excel(writer, sheet_name='uf-max-arrecad', index=False)
        dfe.to_excel(writer, sheet_name='uf-tx-sucesso', index=False)
'''
def exportar_ranking_flex_uf(args, con, caminho_analises_excel)
'''
def exportar_ranking_flex_uf(args, con, caminho_analises_excel):
    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/03-a-ranking-flex-uf-qtd.sql')
    res = con.sql(sql)
    dfa = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/03-b-ranking-flex-uf-tot-arrecad.sql')
    res = con.sql(sql)
    dfb = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/03-c-ranking-flex-uf-avg-arrecad.sql')
    res = con.sql(sql)
    dfc = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/03-d-ranking-flex-uf-max-arrecad.sql')
    res = con.sql(sql)
    dfd = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/03-e-ranking-flex-uf-tx-sucesso.sql')
    res = con.sql(sql)
    dfe = res.to_df()

    with pd.ExcelWriter(f'{caminho_analises_excel}/03-ranking-uf-flex.xlsx') as writer:  
        dfa.to_excel(writer, sheet_name='uf-qtd', index=False)
        dfb.to_excel(writer, sheet_name='uf-tot-arrecad', index=False)
        dfc.to_excel(writer, sheet_name='uf-avg-arrecad', index=False)
        dfd.to_excel(writer, sheet_name='uf-max-arrecad', index=False)
        dfe.to_excel(writer, sheet_name='uf-tx-sucesso', index=False)

'''
def exportar_ranking_rec_uf(args, con, caminho_analises_excel)
'''
def exportar_ranking_rec_uf(args, con, caminho_analises_excel):
    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/04-a-ranking-rec-uf-qtd.sql')
    res = con.sql(sql)
    dfa = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/04-b-ranking-rec-uf-tot-arrecad.sql')
    res = con.sql(sql)
    dfb = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/04-c-ranking-rec-uf-avg-arrecad.sql')
    res = con.sql(sql)
    dfc = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/04-d-ranking-rec-uf-max-arrecad.sql')
    res = con.sql(sql)
    dfd = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/04-e-ranking-rec-uf-tx-sucesso.sql')
    res = con.sql(sql)
    dfe = res.to_df()

    with pd.ExcelWriter(f'{caminho_analises_excel}/04-ranking-uf-rec.xlsx') as writer:  
        dfa.to_excel(writer, sheet_name='uf-qtd', index=False)
        dfb.to_excel(writer, sheet_name='uf-tot-arrecad', index=False)
        dfc.to_excel(writer, sheet_name='uf-avg-arrecad', index=False)
        dfd.to_excel(writer, sheet_name='uf-max-arrecad', index=False)
        dfe.to_excel(writer, sheet_name='uf-tx-sucesso', index=False)


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
    exportar_ranking_tdn_uf(args, con, caminho_analises_excel)
    exportar_ranking_tdn_classificacao_autoria(args, con, caminho_analises_excel)
    exportar_ranking_tdn_autor(args, con, caminho_analises_excel)
    
    exportar_ranking_tdn_categoria_mencao(args, con, caminho_analises_excel)
    exportar_ranking_flex_uf(args, con, caminho_analises_excel)
    exportar_ranking_rec_uf(args, con, caminho_analises_excel)


    p2 = datetime.now()
    delta = p2-p1
    tempo = delta.seconds + delta.microseconds/1000000

    logs.verbose(args.verbose, f'Tempo: {tempo}s')
