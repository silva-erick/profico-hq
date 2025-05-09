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
    
    lote = comum.executar_sql_lote(con, comum.CAMINHO_SQL_ANALISES_SERIES, {
        "11-a-visao-geral-plataformas.sql":"plataforma"
        ,"11-b-visao-geral-modalidade.sql":"modalidade"
        ,"11-c-visao-geral-uf.sql":"uf"
        ,"11-d-visao-geral-classificacao-autoria.sql":"classificacao_autoria"
        ,"11-f-visao-geral-categoria.sql":"categoria"
    })

    comum.gerar_excel_lote(args, f'{caminho_analises_result}/11-visao-geral', '01-visao-geral.xlsx', lote)


def exportar_serie_modalidade(args, con, caminho_analises_result):
    """
    def exportar_serie_modalidade(args, con, caminho_analises_result)
    """
    
    lote = comum.executar_sql_lote(con, comum.CAMINHO_SQL_ANALISES_SERIES, {
        "21-a-modalidade-tudo-ou-nada.sql":"tudo-ou-nada"
        ,"21-b-modalidade-flex.sql":"flex"
        ,"21-c-modalidade-recorrente.sql":"recorrente"
    })

    comum.gerar_excel_lote(args, f'{caminho_analises_result}/21-modalidade', '01-modalidade.xlsx', lote)


def exportar_serie_uf(args, con, caminho_analises_result):
    """
    def exportar_serie_uf(args, con, caminho_analises_result)
    """
    
    lote = comum.executar_sql_lote(con, comum.CAMINHO_SQL_ANALISES_SERIES, {
        "31-a-uf-tudo-ou-nada.sql":"tudo-ou-nada"
        ,"31-b-uf-flex.sql":"flex"
        ,"31-c-uf-recorrente.sql":"recorrente"
    })

    comum.gerar_excel_lote(args, f'{caminho_analises_result}/31-uf', '01-uf.xlsx', lote)


def exportar_serie_classificacao_autoria(args, con, caminho_analises_result):
    """
    def exportar_serie_classificacao_autoria(args, con, caminho_analises_result)
    """
    
    lote = comum.executar_sql_lote(con, comum.CAMINHO_SQL_ANALISES_SERIES, {
        "41-a-classificacao-autoria-tudo-ou-nada.sql":"tudo-ou-nada"
        ,"41-b-classificacao-autoria-flex.sql":"flex"
        ,"41-c-classificacao-autoria-recorrente.sql":"recorrente"
    })

    comum.gerar_excel_lote(args, f'{caminho_analises_result}/41-classificacao-autoria', '01-classificacao-autoria.xlsx', lote)


def exportar_serie_categoria(args, con, caminho_analises_result):
    """
    def exportar_serie_categoria(args, con, caminho_analises_result)
    """
    
    lote = comum.executar_sql_lote(con, comum.CAMINHO_SQL_ANALISES_SERIES, {
        "51-a-categoria-tudo-ou-nada.sql":"tudo-ou-nada"
        ,"51-b-categoria-flex.sql":"flex"
        ,"51-c-categoria-recorrente.sql":"recorrente"
    })

    comum.gerar_excel_lote(args, f'{caminho_analises_result}/51-categoria', '01-categoria.xlsx', lote)
