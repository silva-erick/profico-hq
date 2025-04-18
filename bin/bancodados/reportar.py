import os
import duckdb
import logs
import json
from datetime import datetime, timedelta
import formatos

import pandas as pd


CAMINHO_SQL = "./bancodados/sql"
CAMINHO_SQL_ANALISES = "./bancodados/sql/03-analises"
CAMINHO_SQL_ANALISES_SERIES = "./bancodados/sql/04-analises-serie"
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

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/01-a-visao-geral-modalidade.sql')
    res = con.sql(sql)
    dfa = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/01-b-visao-geral-plataformas.sql')
    res = con.sql(sql)
    dfb = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/01-c-visao-geral-uf.sql')
    res = con.sql(sql)
    dfc = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/01-d-visao-geral-classificacao-autoria.sql')
    res = con.sql(sql)
    dfd = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/01-e-visao-geral-autor.sql')
    res = con.sql(sql)
    dfe = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES}/01-f-visao-geral-categoria-mencao.sql')
    res = con.sql(sql)
    dff = res.to_df()

    with pd.ExcelWriter(f'{caminho_analises_excel}/01-visao-geral.xlsx') as writer:  
        dfa.to_excel(writer, sheet_name='modalidade', index=False)
        #dfb.to_excel(writer, sheet_name='plataforma', index=False)
        dfc.to_excel(writer, sheet_name='uf', index=False)
        dfd.to_excel(writer, sheet_name='classificacao_autoria', index=False)
        dfe.to_excel(writer, sheet_name='autoria', index=False)
        dff.to_excel(writer, sheet_name='categoria_mencao', index=False)

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
        dfa.to_excel(writer, sheet_name='qtd', index=False)
        dfb.to_excel(writer, sheet_name='tot-arrecad', index=False)
        dfc.to_excel(writer, sheet_name='avg-arrecad', index=False)
        dfd.to_excel(writer, sheet_name='max-arrecad', index=False)
        dfe.to_excel(writer, sheet_name='tx-sucesso', index=False)

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
        dfa.to_excel(writer, sheet_name='qtd', index=False)
        dfb.to_excel(writer, sheet_name='tot-arrecad', index=False)
        dfc.to_excel(writer, sheet_name='avg-arrecad', index=False)
        dfd.to_excel(writer, sheet_name='max-arrecad', index=False)
        dfe.to_excel(writer, sheet_name='tx-sucesso', index=False)

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
        dfa.to_excel(writer, sheet_name='qtd', index=False)
        dfb.to_excel(writer, sheet_name='tot-arrecad', index=False)
        dfc.to_excel(writer, sheet_name='avg-arrecad', index=False)
        dfd.to_excel(writer, sheet_name='max-arrecad', index=False)
        dfe.to_excel(writer, sheet_name='tx-sucesso', index=False)

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
        dfa.to_excel(writer, sheet_name='qtd', index=False)
        dfb.to_excel(writer, sheet_name='tot-arrecad', index=False)
        dfc.to_excel(writer, sheet_name='avg-arrecad', index=False)
        dfd.to_excel(writer, sheet_name='max-arrecad', index=False)
        dfe.to_excel(writer, sheet_name='tx-sucesso', index=False)

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
        dfa.to_excel(writer, sheet_name='qtd', index=False)
        dfb.to_excel(writer, sheet_name='tot-arrecad', index=False)
        dfc.to_excel(writer, sheet_name='avg-arrecad', index=False)
        dfd.to_excel(writer, sheet_name='max-arrecad', index=False)
        dfe.to_excel(writer, sheet_name='tx-sucesso', index=False)

'''
def exportar_ranking_flex_classificacao_autoria(args, con, caminho_analises_excel)
'''
def exportar_ranking_flex_classificacao_autoria(args, con, caminho_analises_excel):
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

    with pd.ExcelWriter(f'{caminho_analises_excel}/03-ranking-classificacao-autoria-flex.xlsx') as writer:  
        dfa.to_excel(writer, sheet_name='qtd', index=False)
        dfb.to_excel(writer, sheet_name='tot-arrecad', index=False)
        dfc.to_excel(writer, sheet_name='avg-arrecad', index=False)
        dfd.to_excel(writer, sheet_name='max-arrecad', index=False)
        dfe.to_excel(writer, sheet_name='tx-sucesso', index=False)

'''
def exportar_ranking_flex_autor(args, con, caminho_analises_excel)
'''
def exportar_ranking_flex_autor(args, con, caminho_analises_excel):
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

    with pd.ExcelWriter(f'{caminho_analises_excel}/03-ranking-autor-flex.xlsx') as writer:  
        dfa.to_excel(writer, sheet_name='qtd', index=False)
        dfb.to_excel(writer, sheet_name='tot-arrecad', index=False)
        dfc.to_excel(writer, sheet_name='avg-arrecad', index=False)
        dfd.to_excel(writer, sheet_name='max-arrecad', index=False)
        dfe.to_excel(writer, sheet_name='tx-sucesso', index=False)

'''
def exportar_ranking_flex_categoria_mencao(args, con, caminho_analises_excel)
'''
def exportar_ranking_flex_categoria_mencao(args, con, caminho_analises_excel):
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

    with pd.ExcelWriter(f'{caminho_analises_excel}/03-ranking-categoria-mencao-flex.xlsx') as writer:  
        dfa.to_excel(writer, sheet_name='qtd', index=False)
        dfb.to_excel(writer, sheet_name='tot-arrecad', index=False)
        dfc.to_excel(writer, sheet_name='avg-arrecad', index=False)
        dfd.to_excel(writer, sheet_name='max-arrecad', index=False)
        dfe.to_excel(writer, sheet_name='tx-sucesso', index=False)



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
        dfa.to_excel(writer, sheet_name='qtd', index=False)
        dfb.to_excel(writer, sheet_name='tot-arrecad', index=False)
        dfc.to_excel(writer, sheet_name='avg-arrecad', index=False)
        dfd.to_excel(writer, sheet_name='max-arrecad', index=False)
        dfe.to_excel(writer, sheet_name='tx-sucesso', index=False)


'''
def exportar_ranking_rec_classificacao_autoria(args, con, caminho_analises_excel)
'''
def exportar_ranking_rec_classificacao_autoria(args, con, caminho_analises_excel):
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

    with pd.ExcelWriter(f'{caminho_analises_excel}/04-ranking-classificacao-autoria-rec.xlsx') as writer:  
        dfa.to_excel(writer, sheet_name='qtd', index=False)
        dfb.to_excel(writer, sheet_name='tot-arrecad', index=False)
        dfc.to_excel(writer, sheet_name='avg-arrecad', index=False)
        dfd.to_excel(writer, sheet_name='max-arrecad', index=False)
        dfe.to_excel(writer, sheet_name='tx-sucesso', index=False)

'''
def exportar_ranking_rec_autor(args, con, caminho_analises_excel)
'''
def exportar_ranking_rec_autor(args, con, caminho_analises_excel):
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

    with pd.ExcelWriter(f'{caminho_analises_excel}/04-ranking-autor-rec.xlsx') as writer:  
        dfa.to_excel(writer, sheet_name='qtd', index=False)
        dfb.to_excel(writer, sheet_name='tot-arrecad', index=False)
        dfc.to_excel(writer, sheet_name='avg-arrecad', index=False)
        dfd.to_excel(writer, sheet_name='max-arrecad', index=False)
        dfe.to_excel(writer, sheet_name='tx-sucesso', index=False)

'''
def exportar_ranking_rec_categoria_mencao(args, con, caminho_analises_excel)
'''
def exportar_ranking_rec_categoria_mencao(args, con, caminho_analises_excel):
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

    with pd.ExcelWriter(f'{caminho_analises_excel}/04-ranking-categoria-mencao-rec.xlsx') as writer:  
        dfa.to_excel(writer, sheet_name='qtd', index=False)
        dfb.to_excel(writer, sheet_name='tot-arrecad', index=False)
        dfc.to_excel(writer, sheet_name='avg-arrecad', index=False)
        dfd.to_excel(writer, sheet_name='max-arrecad', index=False)
        dfe.to_excel(writer, sheet_name='tx-sucesso', index=False)





'''
def exportar_serie_visao_geral(args, con, caminho_analises_excel)
'''
def exportar_serie_visao_geral(args, con, caminho_analises_excel):
    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES_SERIES}/11-a-visao-geral-plataformas.sql')
    res = con.sql(sql)
    dfa = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES_SERIES}/11-b-visao-geral-modalidade.sql')
    res = con.sql(sql)
    dfb = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES_SERIES}/11-c-visao-geral-uf.sql')
    res = con.sql(sql)
    dfc = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES_SERIES}/11-d-visao-geral-classificacao-autoria.sql')
    res = con.sql(sql)
    dfd = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES_SERIES}/11-f-visao-geral-categoria-mencao.sql')
    res = con.sql(sql)
    dff = res.to_df()

    with pd.ExcelWriter(f'{caminho_analises_excel}/11-serie-visao-geral.xlsx') as writer:  
        dfa.to_excel(writer, sheet_name='plataforma', index=False)
        dfb.to_excel(writer, sheet_name='modalidade', index=False)
        dfc.to_excel(writer, sheet_name='uf', index=False)
        dfd.to_excel(writer, sheet_name='classificacao_autoria', index=False)
        dff.to_excel(writer, sheet_name='categoria_mencao', index=False)


'''
def exportar_serie_modalidade(args, con, caminho_analises_excel)
'''
def exportar_serie_modalidade(args, con, caminho_analises_excel):
    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES_SERIES}/21-a-modalidade-tudo-ou-nada.sql')
    res = con.sql(sql)
    dfa = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES_SERIES}/21-b-modalidade-flex.sql')
    res = con.sql(sql)
    dfb = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES_SERIES}/21-c-modalidade-recorrente.sql')
    res = con.sql(sql)
    dfc = res.to_df()

    with pd.ExcelWriter(f'{caminho_analises_excel}/21-serie-modalidade.xlsx') as writer:  
        dfa.to_excel(writer, sheet_name='tudo-ou-nada', index=False)
        dfb.to_excel(writer, sheet_name='flex', index=False)
        dfc.to_excel(writer, sheet_name='recorrente', index=False)


'''
def exportar_serie_uf(args, con, caminho_analises_excel)
'''
def exportar_serie_uf(args, con, caminho_analises_excel):
    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES_SERIES}/31-a-uf-tudo-ou-nada.sql')
    res = con.sql(sql)
    dfa = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES_SERIES}/31-b-uf-flex.sql')
    res = con.sql(sql)
    dfb = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES_SERIES}/31-c-uf-recorrente.sql')
    res = con.sql(sql)
    dfc = res.to_df()

    with pd.ExcelWriter(f'{caminho_analises_excel}/31-serie-uf.xlsx') as writer:  
        dfa.to_excel(writer, sheet_name='tudo-ou-nada', index=False)
        dfb.to_excel(writer, sheet_name='flex', index=False)
        dfc.to_excel(writer, sheet_name='recorrente', index=False)


'''
def exportar_serie_classificacao_autoria(args, con, caminho_analises_excel)
'''
def exportar_serie_classificacao_autoria(args, con, caminho_analises_excel):
    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES_SERIES}/41-a-classificacao-autoria-tudo-ou-nada.sql')
    res = con.sql(sql)
    dfa = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES_SERIES}/41-b-classificacao-autoria-flex.sql')
    res = con.sql(sql)
    dfb = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES_SERIES}/41-c-classificacao-autoria-recorrente.sql')
    res = con.sql(sql)
    dfc = res.to_df()

    with pd.ExcelWriter(f'{caminho_analises_excel}/41-serie-classificacao-autoria.xlsx') as writer:  
        dfa.to_excel(writer, sheet_name='tudo-ou-nada', index=False)
        dfb.to_excel(writer, sheet_name='flex', index=False)
        dfc.to_excel(writer, sheet_name='recorrente', index=False)


'''
def exportar_serie_categoria_mencao(args, con, caminho_analises_excel)
'''
def exportar_serie_categoria_mencao(args, con, caminho_analises_excel):
    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES_SERIES}/51-a-categoria-mencao-tudo-ou-nada.sql')
    res = con.sql(sql)
    dfa = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES_SERIES}/51-b-categoria-mencao-flex.sql')
    res = con.sql(sql)
    dfb = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES_SERIES}/51-c-categoria-mencao-recorrente.sql')
    res = con.sql(sql)
    dfc = res.to_df()

    with pd.ExcelWriter(f'{caminho_analises_excel}/51-serie-categoria-mencao.xlsx') as writer:  
        dfa.to_excel(writer, sheet_name='tudo-ou-nada', index=False)
        dfb.to_excel(writer, sheet_name='flex', index=False)
        dfc.to_excel(writer, sheet_name='recorrente', index=False)


'''
async def executar_report(args)
-- 
'''
async def executar_report(args):
    p1 = datetime.now()

    caminho_analises = f"{CAMINHO_ANALISES}/{args.ano}"
    caminho_analises_excel = f"{caminho_analises}/excel"

    caminho_arq = f"{caminho_analises}/analises_{args.ano}.duckdb"

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
    exportar_ranking_flex_classificacao_autoria(args, con, caminho_analises_excel)
    exportar_ranking_flex_autor(args, con, caminho_analises_excel)    
    exportar_ranking_flex_categoria_mencao(args, con, caminho_analises_excel)

    exportar_ranking_rec_uf(args, con, caminho_analises_excel)
    exportar_ranking_rec_classificacao_autoria(args, con, caminho_analises_excel)
    exportar_ranking_rec_autor(args, con, caminho_analises_excel)    
    exportar_ranking_rec_categoria_mencao(args, con, caminho_analises_excel)

    exportar_serie_visao_geral(args, con, caminho_analises_excel)
    exportar_serie_modalidade(args, con, caminho_analises_excel)
    exportar_serie_uf(args, con, caminho_analises_excel)
    exportar_serie_classificacao_autoria(args, con, caminho_analises_excel)
    exportar_serie_categoria_mencao(args, con, caminho_analises_excel)

    p2 = datetime.now()
    delta = p2-p1
    tempo = delta.seconds + delta.microseconds/1000000

    logs.verbose(args.verbose, f'Tempo: {tempo}s')
