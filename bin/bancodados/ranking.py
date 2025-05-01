import pandas as pd
import bancodados.comum as comum
import pydot
import duckdb
import formatos

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import time



"""
def exportar_ranking_tdn_uf(args, con, caminho_analises_result)
"""
def exportar_ranking_tdn_uf(args, con, caminho_analises_result):
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

    with pd.ExcelWriter(f'{caminho_analises_result}/02-ranking-uf-tdn.xlsx') as writer:  
        dfa.to_excel(writer, sheet_name='qtd', index=False)
        dfb.to_excel(writer, sheet_name='tot-arrecad', index=False)
        dfc.to_excel(writer, sheet_name='avg-arrecad', index=False)
        dfd.to_excel(writer, sheet_name='max-arrecad', index=False)
        dfe.to_excel(writer, sheet_name='tx-sucesso', index=False)

"""
def exportar_ranking_tdn_classificacao_autoria(args, con, caminho_analises_result)
"""
def exportar_ranking_tdn_classificacao_autoria(args, con, caminho_analises_result):
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

    with pd.ExcelWriter(f'{caminho_analises_result}/02-ranking-classificacao-autoria-tdn.xlsx') as writer:  
        dfa.to_excel(writer, sheet_name='qtd', index=False)
        dfb.to_excel(writer, sheet_name='tot-arrecad', index=False)
        dfc.to_excel(writer, sheet_name='avg-arrecad', index=False)
        dfd.to_excel(writer, sheet_name='max-arrecad', index=False)
        dfe.to_excel(writer, sheet_name='tx-sucesso', index=False)

"""
def exportar_ranking_tdn_autor(args, con, caminho_analises_result)
"""
def exportar_ranking_tdn_autor(args, con, caminho_analises_result):
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

    with pd.ExcelWriter(f'{caminho_analises_result}/02-ranking-autor-tdn.xlsx') as writer:  
        dfa.to_excel(writer, sheet_name='qtd', index=False)
        dfb.to_excel(writer, sheet_name='tot-arrecad', index=False)
        dfc.to_excel(writer, sheet_name='avg-arrecad', index=False)
        dfd.to_excel(writer, sheet_name='max-arrecad', index=False)
        dfe.to_excel(writer, sheet_name='tx-sucesso', index=False)

"""
def exportar_ranking_tdn_categoria_mencao(args, con, caminho_analises_result)
"""
def exportar_ranking_tdn_categoria_mencao(args, con, caminho_analises_result):
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

    with pd.ExcelWriter(f'{caminho_analises_result}/02-ranking-categoria-mencao-tdn.xlsx') as writer:  
        dfa.to_excel(writer, sheet_name='qtd', index=False)
        dfb.to_excel(writer, sheet_name='tot-arrecad', index=False)
        dfc.to_excel(writer, sheet_name='avg-arrecad', index=False)
        dfd.to_excel(writer, sheet_name='max-arrecad', index=False)
        dfe.to_excel(writer, sheet_name='tx-sucesso', index=False)

"""
def exportar_ranking_flex_uf(args, con, caminho_analises_result)
"""
def exportar_ranking_flex_uf(args, con, caminho_analises_result):
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

    with pd.ExcelWriter(f'{caminho_analises_result}/03-ranking-uf-flex.xlsx') as writer:  
        dfa.to_excel(writer, sheet_name='qtd', index=False)
        dfb.to_excel(writer, sheet_name='tot-arrecad', index=False)
        dfc.to_excel(writer, sheet_name='avg-arrecad', index=False)
        dfd.to_excel(writer, sheet_name='max-arrecad', index=False)
        dfe.to_excel(writer, sheet_name='tx-sucesso', index=False)

"""
def exportar_ranking_flex_classificacao_autoria(args, con, caminho_analises_result)
"""
def exportar_ranking_flex_classificacao_autoria(args, con, caminho_analises_result):
    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/03-f-ranking-flex-classificacao-autoria-qtd.sql')
    res = con.sql(sql)
    dfa = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/03-g-ranking-flex-classificacao-autoria-tot-arrecad.sql')
    res = con.sql(sql)
    dfb = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/03-h-ranking-flex-classificacao-autoria-avg-arrecad.sql')
    res = con.sql(sql)
    dfc = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/03-i-ranking-flex-classificacao-autoria-max-arrecad.sql')
    res = con.sql(sql)
    dfd = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/03-j-ranking-flex-classificacao-autoria-tx-sucesso.sql')
    res = con.sql(sql)
    dfe = res.to_df()

    with pd.ExcelWriter(f'{caminho_analises_result}/03-ranking-classificacao-autoria-flex.xlsx') as writer:  
        dfa.to_excel(writer, sheet_name='qtd', index=False)
        dfb.to_excel(writer, sheet_name='tot-arrecad', index=False)
        dfc.to_excel(writer, sheet_name='avg-arrecad', index=False)
        dfd.to_excel(writer, sheet_name='max-arrecad', index=False)
        dfe.to_excel(writer, sheet_name='tx-sucesso', index=False)

"""
def exportar_ranking_flex_autor(args, con, caminho_analises_result)
"""
def exportar_ranking_flex_autor(args, con, caminho_analises_result):
    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/03-k-ranking-flex-autor-qtd.sql')
    res = con.sql(sql)
    dfa = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/03-l-ranking-flex-autor-tot-arrecad.sql')
    res = con.sql(sql)
    dfb = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/03-m-ranking-flex-autor-avg-arrecad.sql')
    res = con.sql(sql)
    dfc = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/03-n-ranking-flex-autor-max-arrecad.sql')
    res = con.sql(sql)
    dfd = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/03-o-ranking-flex-autor-tx-sucesso.sql')
    res = con.sql(sql)
    dfe = res.to_df()

    with pd.ExcelWriter(f'{caminho_analises_result}/03-ranking-autor-flex.xlsx') as writer:  
        dfa.to_excel(writer, sheet_name='qtd', index=False)
        dfb.to_excel(writer, sheet_name='tot-arrecad', index=False)
        dfc.to_excel(writer, sheet_name='avg-arrecad', index=False)
        dfd.to_excel(writer, sheet_name='max-arrecad', index=False)
        dfe.to_excel(writer, sheet_name='tx-sucesso', index=False)

"""
def exportar_ranking_flex_categoria_mencao(args, con, caminho_analises_result)
"""
def exportar_ranking_flex_categoria_mencao(args, con, caminho_analises_result):
    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/03-p-ranking-flex-categoria-mencao-qtd.sql')
    res = con.sql(sql)
    dfa = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/03-q-ranking-flex-categoria-mencao-tot-arrecad.sql')
    res = con.sql(sql)
    dfb = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/03-r-ranking-flex-categoria-mencao-avg-arrecad.sql')
    res = con.sql(sql)
    dfc = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/03-s-ranking-flex-categoria-mencao-max-arrecad.sql')
    res = con.sql(sql)
    dfd = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/03-t-ranking-flex-categoria-mencao-tx-sucesso.sql')
    res = con.sql(sql)
    dfe = res.to_df()

    with pd.ExcelWriter(f'{caminho_analises_result}/03-ranking-categoria-mencao-flex.xlsx') as writer:  
        dfa.to_excel(writer, sheet_name='qtd', index=False)
        dfb.to_excel(writer, sheet_name='tot-arrecad', index=False)
        dfc.to_excel(writer, sheet_name='avg-arrecad', index=False)
        dfd.to_excel(writer, sheet_name='max-arrecad', index=False)
        dfe.to_excel(writer, sheet_name='tx-sucesso', index=False)



"""
def exportar_ranking_rec_uf(args, con, caminho_analises_result)
"""
def exportar_ranking_rec_uf(args, con, caminho_analises_result):
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

    with pd.ExcelWriter(f'{caminho_analises_result}/04-ranking-uf-rec.xlsx') as writer:  
        dfa.to_excel(writer, sheet_name='qtd', index=False)
        dfb.to_excel(writer, sheet_name='tot-arrecad', index=False)
        dfc.to_excel(writer, sheet_name='avg-arrecad', index=False)
        dfd.to_excel(writer, sheet_name='max-arrecad', index=False)
        dfe.to_excel(writer, sheet_name='tx-sucesso', index=False)


"""
def exportar_ranking_rec_classificacao_autoria(args, con, caminho_analises_result)
"""
def exportar_ranking_rec_classificacao_autoria(args, con, caminho_analises_result):
    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/04-f-ranking-rec-classificacao-autoria-qtd.sql')
    res = con.sql(sql)
    dfa = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/04-g-ranking-rec-classificacao-autoria-tot-arrecad.sql')
    res = con.sql(sql)
    dfb = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/04-h-ranking-rec-classificacao-autoria-avg-arrecad.sql')
    res = con.sql(sql)
    dfc = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/04-i-ranking-rec-classificacao-autoria-max-arrecad.sql')
    res = con.sql(sql)
    dfd = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/04-j-ranking-rec-classificacao-autoria-tx-sucesso.sql')
    res = con.sql(sql)
    dfe = res.to_df()

    with pd.ExcelWriter(f'{caminho_analises_result}/04-ranking-classificacao-autoria-rec.xlsx') as writer:  
        dfa.to_excel(writer, sheet_name='qtd', index=False)
        dfb.to_excel(writer, sheet_name='tot-arrecad', index=False)
        dfc.to_excel(writer, sheet_name='avg-arrecad', index=False)
        dfd.to_excel(writer, sheet_name='max-arrecad', index=False)
        dfe.to_excel(writer, sheet_name='tx-sucesso', index=False)

"""
def exportar_ranking_rec_autor(args, con, caminho_analises_result)
"""
def exportar_ranking_rec_autor(args, con, caminho_analises_result):
    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/04-k-ranking-rec-autor-qtd.sql')
    res = con.sql(sql)
    dfa = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/04-l-ranking-rec-autor-tot-arrecad.sql')
    res = con.sql(sql)
    dfb = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/04-m-ranking-rec-autor-avg-arrecad.sql')
    res = con.sql(sql)
    dfc = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/04-n-ranking-rec-autor-max-arrecad.sql')
    res = con.sql(sql)
    dfd = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/04-o-ranking-rec-autor-tx-sucesso.sql')
    res = con.sql(sql)
    dfe = res.to_df()

    with pd.ExcelWriter(f'{caminho_analises_result}/04-ranking-autor-rec.xlsx') as writer:  
        dfa.to_excel(writer, sheet_name='qtd', index=False)
        dfb.to_excel(writer, sheet_name='tot-arrecad', index=False)
        dfc.to_excel(writer, sheet_name='avg-arrecad', index=False)
        dfd.to_excel(writer, sheet_name='max-arrecad', index=False)
        dfe.to_excel(writer, sheet_name='tx-sucesso', index=False)

"""
def exportar_ranking_rec_categoria_mencao(args, con, caminho_analises_result)
"""
def exportar_ranking_rec_categoria_mencao(args, con, caminho_analises_result):
    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/04-p-ranking-rec-categoria-mencao-qtd.sql')
    res = con.sql(sql)
    dfa = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/04-q-ranking-rec-categoria-mencao-tot-arrecad.sql')
    res = con.sql(sql)
    dfb = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/04-r-ranking-rec-categoria-mencao-avg-arrecad.sql')
    res = con.sql(sql)
    dfc = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/04-s-ranking-rec-categoria-mencao-max-arrecad.sql')
    res = con.sql(sql)
    dfd = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/04-t-ranking-rec-categoria-mencao-tx-sucesso.sql')
    res = con.sql(sql)
    dfe = res.to_df()

    with pd.ExcelWriter(f'{caminho_analises_result}/04-ranking-categoria-mencao-rec.xlsx') as writer:  
        dfa.to_excel(writer, sheet_name='qtd', index=False)
        dfb.to_excel(writer, sheet_name='tot-arrecad', index=False)
        dfc.to_excel(writer, sheet_name='avg-arrecad', index=False)
        dfd.to_excel(writer, sheet_name='max-arrecad', index=False)
        dfe.to_excel(writer, sheet_name='tx-sucesso', index=False)
