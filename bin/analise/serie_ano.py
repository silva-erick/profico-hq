import os
import duckdb
import logs
import json
from datetime import datetime, timedelta
import formatos
import arquivos

import pandas as pd

import pydot

import analise.comum as comum
import analise.dados_campanhas as dados_campanhas
import analise.visao_geral as visao_geral

def exportar_serie_visao_geral(args, con, caminho_analises_result):
    """
    def exportar_serie_visao_geral(args, con, caminho_analises_result)
    """
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

    with pd.ExcelWriter(f'{caminho_analises_result}/11-serie-visao-geral.xlsx') as writer:  
        dfa.to_excel(writer, sheet_name='plataforma', index=False)
        dfb.to_excel(writer, sheet_name='modalidade', index=False)
        dfc.to_excel(writer, sheet_name='uf', index=False)
        dfd.to_excel(writer, sheet_name='classificacao_autoria', index=False)
        dff.to_excel(writer, sheet_name='categoria_mencao', index=False)


def exportar_serie_modalidade(args, con, caminho_analises_result):
    """
    def exportar_serie_modalidade(args, con, caminho_analises_result)
    """
    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES_SERIES}/21-a-modalidade-tudo-ou-nada.sql')
    res = con.sql(sql)
    dfa = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES_SERIES}/21-b-modalidade-flex.sql')
    res = con.sql(sql)
    dfb = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES_SERIES}/21-c-modalidade-recorrente.sql')
    res = con.sql(sql)
    dfc = res.to_df()

    with pd.ExcelWriter(f'{caminho_analises_result}/21-serie-modalidade.xlsx') as writer:  
        dfa.to_excel(writer, sheet_name='tudo-ou-nada', index=False)
        dfb.to_excel(writer, sheet_name='flex', index=False)
        dfc.to_excel(writer, sheet_name='recorrente', index=False)


def exportar_serie_uf(args, con, caminho_analises_result):
    """
    def exportar_serie_uf(args, con, caminho_analises_result)
    """
    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES_SERIES}/31-a-uf-tudo-ou-nada.sql')
    res = con.sql(sql)
    dfa = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES_SERIES}/31-b-uf-flex.sql')
    res = con.sql(sql)
    dfb = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES_SERIES}/31-c-uf-recorrente.sql')
    res = con.sql(sql)
    dfc = res.to_df()

    with pd.ExcelWriter(f'{caminho_analises_result}/31-serie-uf.xlsx') as writer:  
        dfa.to_excel(writer, sheet_name='tudo-ou-nada', index=False)
        dfb.to_excel(writer, sheet_name='flex', index=False)
        dfc.to_excel(writer, sheet_name='recorrente', index=False)


def exportar_serie_classificacao_autoria(args, con, caminho_analises_result):
    """
    def exportar_serie_classificacao_autoria(args, con, caminho_analises_result)
    """
    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES_SERIES}/41-a-classificacao-autoria-tudo-ou-nada.sql')
    res = con.sql(sql)
    dfa = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES_SERIES}/41-b-classificacao-autoria-flex.sql')
    res = con.sql(sql)
    dfb = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES_SERIES}/41-c-classificacao-autoria-recorrente.sql')
    res = con.sql(sql)
    dfc = res.to_df()

    with pd.ExcelWriter(f'{caminho_analises_result}/41-serie-classificacao-autoria.xlsx') as writer:  
        dfa.to_excel(writer, sheet_name='tudo-ou-nada', index=False)
        dfb.to_excel(writer, sheet_name='flex', index=False)
        dfc.to_excel(writer, sheet_name='recorrente', index=False)


def exportar_serie_categoria_mencao(args, con, caminho_analises_result):
    """
    def exportar_serie_categoria_mencao(args, con, caminho_analises_result)
    """
    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES_SERIES}/51-a-categoria-mencao-tudo-ou-nada.sql')
    res = con.sql(sql)
    dfa = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES_SERIES}/51-b-categoria-mencao-flex.sql')
    res = con.sql(sql)
    dfb = res.to_df()

    sql = ler_arquivo(f'{CAMINHO_SQL_ANALISES_SERIES}/51-c-categoria-mencao-recorrente.sql')
    res = con.sql(sql)
    dfc = res.to_df()

    with pd.ExcelWriter(f'{caminho_analises_result}/51-serie-categoria-mencao.xlsx') as writer:  
        dfa.to_excel(writer, sheet_name='tudo-ou-nada', index=False)
        dfb.to_excel(writer, sheet_name='flex', index=False)
        dfc.to_excel(writer, sheet_name='recorrente', index=False)


def exportar_serie_visao_geral(args, con, caminho_analises_result):
    """
    def exportar_serie_visao_geral(args, con, caminho_analises_result)
    """
    sql = ler_arquivo(f'{comum.CAMINHO_SQL_ANALISES_SERIES}/11-a-visao-geral-plataformas.sql')
    res = con.sql(sql)
    dfa = res.to_df()

    sql = ler_arquivo(f'{comum.CAMINHO_SQL_ANALISES_SERIES}/11-b-visao-geral-modalidade.sql')
    res = con.sql(sql)
    dfb = res.to_df()

    sql = ler_arquivo(f'{comum.CAMINHO_SQL_ANALISES_SERIES}/11-c-visao-geral-uf.sql')
    res = con.sql(sql)
    dfc = res.to_df()

    sql = ler_arquivo(f'{comum.CAMINHO_SQL_ANALISES_SERIES}/11-d-visao-geral-classificacao-autoria.sql')
    res = con.sql(sql)
    dfd = res.to_df()

    sql = ler_arquivo(f'{comum.CAMINHO_SQL_ANALISES_SERIES}/11-f-visao-geral-categoria-mencao.sql')
    res = con.sql(sql)
    dff = res.to_df()

    with pd.ExcelWriter(f'{caminho_analises_result}/11-serie-visao-geral.xlsx') as writer:  
        dfa.to_excel(writer, sheet_name='plataforma', index=False)
        dfb.to_excel(writer, sheet_name='modalidade', index=False)
        dfc.to_excel(writer, sheet_name='uf', index=False)
        dfd.to_excel(writer, sheet_name='classificacao_autoria', index=False)
        dff.to_excel(writer, sheet_name='categoria_mencao', index=False)


def exportar_serie_modalidade(args, con, caminho_analises_result):
    """
    def exportar_serie_modalidade(args, con, caminho_analises_result)
    """
    sql = ler_arquivo(f'{comum.CAMINHO_SQL_ANALISES_SERIES}/21-a-modalidade-tudo-ou-nada.sql')
    res = con.sql(sql)
    dfa = res.to_df()

    sql = ler_arquivo(f'{comum.CAMINHO_SQL_ANALISES_SERIES}/21-b-modalidade-flex.sql')
    res = con.sql(sql)
    dfb = res.to_df()

    sql = ler_arquivo(f'{comum.CAMINHO_SQL_ANALISES_SERIES}/21-c-modalidade-recorrente.sql')
    res = con.sql(sql)
    dfc = res.to_df()

    with pd.ExcelWriter(f'{caminho_analises_result}/21-serie-modalidade.xlsx') as writer:  
        dfa.to_excel(writer, sheet_name='tudo-ou-nada', index=False)
        dfb.to_excel(writer, sheet_name='flex', index=False)
        dfc.to_excel(writer, sheet_name='recorrente', index=False)


def exportar_serie_uf(args, con, caminho_analises_result):
    """
    def exportar_serie_uf(args, con, caminho_analises_result)
    """
    sql = ler_arquivo(f'{comum.CAMINHO_SQL_ANALISES_SERIES}/31-a-uf-tudo-ou-nada.sql')
    res = con.sql(sql)
    dfa = res.to_df()

    sql = ler_arquivo(f'{comum.CAMINHO_SQL_ANALISES_SERIES}/31-b-uf-flex.sql')
    res = con.sql(sql)
    dfb = res.to_df()

    sql = ler_arquivo(f'{comum.CAMINHO_SQL_ANALISES_SERIES}/31-c-uf-recorrente.sql')
    res = con.sql(sql)
    dfc = res.to_df()

    with pd.ExcelWriter(f'{caminho_analises_result}/31-serie-uf.xlsx') as writer:  
        dfa.to_excel(writer, sheet_name='tudo-ou-nada', index=False)
        dfb.to_excel(writer, sheet_name='flex', index=False)
        dfc.to_excel(writer, sheet_name='recorrente', index=False)


def exportar_serie_classificacao_autoria(args, con, caminho_analises_result):
    """
    def exportar_serie_classificacao_autoria(args, con, caminho_analises_result)
    """
    sql = ler_arquivo(f'{comum.CAMINHO_SQL_ANALISES_SERIES}/41-a-classificacao-autoria-tudo-ou-nada.sql')
    res = con.sql(sql)
    dfa = res.to_df()

    sql = ler_arquivo(f'{comum.CAMINHO_SQL_ANALISES_SERIES}/41-b-classificacao-autoria-flex.sql')
    res = con.sql(sql)
    dfb = res.to_df()

    sql = ler_arquivo(f'{comum.CAMINHO_SQL_ANALISES_SERIES}/41-c-classificacao-autoria-recorrente.sql')
    res = con.sql(sql)
    dfc = res.to_df()

    with pd.ExcelWriter(f'{caminho_analises_result}/41-serie-classificacao-autoria.xlsx') as writer:  
        dfa.to_excel(writer, sheet_name='tudo-ou-nada', index=False)
        dfb.to_excel(writer, sheet_name='flex', index=False)
        dfc.to_excel(writer, sheet_name='recorrente', index=False)


def exportar_serie_categoria_mencao(args, con, caminho_analises_result):
    """
    def exportar_serie_categoria_mencao(args, con, caminho_analises_result)
    """
    sql = ler_arquivo(f'{comum.CAMINHO_SQL_ANALISES_SERIES}/51-a-categoria-mencao-tudo-ou-nada.sql')
    res = con.sql(sql)
    dfa = res.to_df()

    sql = ler_arquivo(f'{comum.CAMINHO_SQL_ANALISES_SERIES}/51-b-categoria-mencao-flex.sql')
    res = con.sql(sql)
    dfb = res.to_df()

    sql = ler_arquivo(f'{comum.CAMINHO_SQL_ANALISES_SERIES}/51-c-categoria-mencao-recorrente.sql')
    res = con.sql(sql)
    dfc = res.to_df()

    with pd.ExcelWriter(f'{caminho_analises_result}/51-serie-categoria-mencao.xlsx') as writer:  
        dfa.to_excel(writer, sheet_name='tudo-ou-nada', index=False)
        dfb.to_excel(writer, sheet_name='flex', index=False)
        dfc.to_excel(writer, sheet_name='recorrente', index=False)
