import pandas as pd
import analise.comum as comum
import pydot
import duckdb
import formatos
import arquivos

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import time


def exportar_ranking_tdn_uf(args, con, caminho_analises_result):
    """
    def exportar_ranking_tdn_uf(args, con, caminho_analises_result)
    """

    lote = comum.executar_sql_lote(con, f'{comum.CAMINHO_SCRIPTS_ANALISES}/02-ranking/', {
        "02-a-ranking-tdn-uf-qtd.sql":"qtd"
        ,"02-b-ranking-tdn-uf-tot-arrecad.sql":"tot-arrecad"
        ,"02-c-ranking-tdn-uf-avg-arrecad.sql":"avg-arrecad"
        ,"02-d-ranking-tdn-uf-max-arrecad.sql":"max-arrecad"
        ,"02-e-ranking-tdn-uf-tx-sucesso.sql":"tx-sucesso"
    })

    comum.gerar_excel_lote(f'{caminho_analises_result}/02-ranking-uf-tdn.xlsx', lote)


def exportar_ranking_tdn_classificacao_autoria(args, con, caminho_analises_result):
    """
    def exportar_ranking_tdn_classificacao_autoria(args, con, caminho_analises_result)
    """

    lote = comum.executar_sql_lote(con, f'{comum.CAMINHO_SCRIPTS_ANALISES}/02-ranking/', {
        "02-f-ranking-tdn-classificacao-autoria-qtd.sql":"qtd"
        ,"02-g-ranking-tdn-classificacao-autoria-tot-arrecad.sql":"tot-arrecad"
        ,"02-h-ranking-tdn-classificacao-autoria-avg-arrecad.sql":"avg-arrecad"
        ,"02-i-ranking-tdn-classificacao-autoria-max-arrecad.sql":"max-arrecad"
        ,"02-j-ranking-tdn-classificacao-autoria-tx-sucesso.sql":"tx-sucesso"
    })

    comum.gerar_excel_lote(f'{caminho_analises_result}/02-ranking-classificacao-autoria-tdn.xlsx', lote)


def exportar_ranking_tdn_autor(args, con, caminho_analises_result):
    """
    def exportar_ranking_tdn_autor(args, con, caminho_analises_result)
    """

    lote = comum.executar_sql_lote(con, f'{comum.CAMINHO_SCRIPTS_ANALISES}/02-ranking/', {
        "02-k-ranking-tdn-autor-qtd.sql":"qtd"
        ,"02-l-ranking-tdn-autor-tot-arrecad.sql":"tot-arrecad"
        ,"02-m-ranking-tdn-autor-avg-arrecad.sql":"avg-arrecad"
        ,"02-n-ranking-tdn-autor-max-arrecad.sql":"max-arrecad"
        ,"02-o-ranking-tdn-autor-tx-sucesso.sql":"tx-sucesso"
    })

    comum.gerar_excel_lote(f'{caminho_analises_result}/02-ranking-autor-tdn.xlsx', lote)


def exportar_ranking_tdn_categoria_mencao(args, con, caminho_analises_result):
    """
    def exportar_ranking_tdn_categoria_mencao(args, con, caminho_analises_result)
    """

    lote = comum.executar_sql_lote(con, f'{comum.CAMINHO_SCRIPTS_ANALISES}/02-ranking/', {
        "02-p-ranking-tdn-categoria-mencao-qtd.sql":"qtd"
        ,"02-q-ranking-tdn-categoria-mencao-tot-arrecad.sql":"tot-arrecad"
        ,"02-r-ranking-tdn-categoria-mencao-avg-arrecad.sql":"avg-arrecad"
        ,"02-s-ranking-tdn-categoria-mencao-max-arrecad.sql":"max-arrecad"
        ,"02-t-ranking-tdn-categoria-mencao-tx-sucesso.sql":"tx-sucesso"
    })

    comum.gerar_excel_lote(f'{caminho_analises_result}/02-ranking-categoria-mencao-tdn.xlsx', lote)


def exportar_ranking_flex_uf(args, con, caminho_analises_result):
    """
    def exportar_ranking_flex_uf(args, con, caminho_analises_result)
    """

    lote = comum.executar_sql_lote(con, f'{comum.CAMINHO_SCRIPTS_ANALISES}/02-ranking/', {
        "03-a-ranking-flex-uf-qtd.sql":"qtd"
        ,"03-b-ranking-flex-uf-tot-arrecad.sql":"tot-arrecad"
        ,"03-c-ranking-flex-uf-avg-arrecad.sql":"avg-arrecad"
        ,"03-d-ranking-flex-uf-max-arrecad.sql":"max-arrecad"
        ,"03-e-ranking-flex-uf-tx-sucesso.sql":"tx-sucesso"
    })

    comum.gerar_excel_lote(f'{caminho_analises_result}/03-ranking-uf-flex.xlsx', lote)


def exportar_ranking_flex_classificacao_autoria(args, con, caminho_analises_result):
    """
    def exportar_ranking_flex_classificacao_autoria(args, con, caminho_analises_result)
    """

    lote = comum.executar_sql_lote(con, f'{comum.CAMINHO_SCRIPTS_ANALISES}/02-ranking/', {
        "03-f-ranking-flex-classificacao-autoria-qtd.sql":"qtd"
        ,"03-g-ranking-flex-classificacao-autoria-tot-arrecad.sql":"tot-arrecad"
        ,"03-h-ranking-flex-classificacao-autoria-avg-arrecad.sql":"avg-arrecad"
        ,"03-i-ranking-flex-classificacao-autoria-max-arrecad.sql":"max-arrecad"
        ,"03-j-ranking-flex-classificacao-autoria-tx-sucesso.sql":"tx-sucesso"
    })

    comum.gerar_excel_lote(f'{caminho_analises_result}/03-ranking-classificacao-autoria-flex.xlsx', lote)


def exportar_ranking_flex_autor(args, con, caminho_analises_result):
    """
    def exportar_ranking_flex_autor(args, con, caminho_analises_result)
    """

    lote = comum.executar_sql_lote(con, f'{comum.CAMINHO_SCRIPTS_ANALISES}/02-ranking/', {
        "03-k-ranking-flex-autor-qtd.sql":"qtd"
        ,"03-l-ranking-flex-autor-tot-arrecad.sql":"tot-arrecad"
        ,"03-m-ranking-flex-autor-avg-arrecad.sql":"avg-arrecad"
        ,"03-n-ranking-flex-autor-max-arrecad.sql":"max-arrecad"
        ,"03-o-ranking-flex-autor-tx-sucesso.sql":"tx-sucesso"
    })

    comum.gerar_excel_lote(f'{caminho_analises_result}/03-ranking-autor-flex.xlsx', lote)


def exportar_ranking_flex_categoria_mencao(args, con, caminho_analises_result):
    """
    def exportar_ranking_flex_categoria_mencao(args, con, caminho_analises_result)
    """

    lote = comum.executar_sql_lote(con, f'{comum.CAMINHO_SCRIPTS_ANALISES}/02-ranking/', {
        "03-p-ranking-flex-categoria-mencao-qtd.sql":"qtd"
        ,"03-q-ranking-flex-categoria-mencao-tot-arrecad.sql":"tot-arrecad"
        ,"03-r-ranking-flex-categoria-mencao-avg-arrecad.sql":"avg-arrecad"
        ,"03-s-ranking-flex-categoria-mencao-max-arrecad.sql":"max-arrecad"
        ,"03-t-ranking-flex-categoria-mencao-tx-sucesso.sql":"tx-sucesso"
    })

    comum.gerar_excel_lote(f'{caminho_analises_result}/03-ranking-categoria-mencao-flex.xlsx', lote)


def exportar_ranking_rec_uf(args, con, caminho_analises_result):
    """
    def exportar_ranking_rec_uf(args, con, caminho_analises_result)
    """

    lote = comum.executar_sql_lote(con, f'{comum.CAMINHO_SCRIPTS_ANALISES}/02-ranking/', {
        "04-a-ranking-rec-uf-qtd.sql":"qtd"
        ,"04-b-ranking-rec-uf-tot-arrecad.sql":"tot-arrecad"
        ,"04-c-ranking-rec-uf-avg-arrecad.sql":"avg-arrecad"
        ,"04-d-ranking-rec-uf-max-arrecad.sql":"max-arrecad"
        ,"04-e-ranking-rec-uf-tx-sucesso.sql":"tx-sucesso"
    })

    comum.gerar_excel_lote(f'{caminho_analises_result}/04-ranking-uf-rec.xlsx', lote)


def exportar_ranking_rec_classificacao_autoria(args, con, caminho_analises_result):
    """
    def exportar_ranking_rec_classificacao_autoria(args, con, caminho_analises_result)
    """

    lote = comum.executar_sql_lote(con, f'{comum.CAMINHO_SCRIPTS_ANALISES}/02-ranking/', {
        "04-f-ranking-rec-classificacao-autoria-qtd.sql":"qtd"
        ,"04-g-ranking-rec-classificacao-autoria-tot-arrecad.sql":"tot-arrecad"
        ,"04-h-ranking-rec-classificacao-autoria-avg-arrecad.sql":"avg-arrecad"
        ,"04-i-ranking-rec-classificacao-autoria-max-arrecad.sql":"max-arrecad"
        ,"04-j-ranking-rec-classificacao-autoria-tx-sucesso.sql":"tx-sucesso"
    })

    comum.gerar_excel_lote(f'{caminho_analises_result}/04-ranking-classificacao-autoria-rec.xlsx', lote)


def exportar_ranking_rec_autor(args, con, caminho_analises_result):
    """
    def exportar_ranking_rec_autor(args, con, caminho_analises_result)
    """

    lote = comum.executar_sql_lote(con, f'{comum.CAMINHO_SCRIPTS_ANALISES}/02-ranking/', {
        "04-k-ranking-rec-autor-qtd.sql":"qtd"
        ,"04-l-ranking-rec-autor-tot-arrecad.sql":"tot-arrecad"
        ,"04-m-ranking-rec-autor-avg-arrecad.sql":"avg-arrecad"
        ,"04-n-ranking-rec-autor-max-arrecad.sql":"max-arrecad"
        ,"04-o-ranking-rec-autor-tx-sucesso.sql":"tx-sucesso"
    })

    comum.gerar_excel_lote(f'{caminho_analises_result}/04-ranking-autor-rec.xlsx', lote)


def exportar_ranking_rec_categoria_mencao(args, con, caminho_analises_result):
    """
    def exportar_ranking_rec_categoria_mencao(args, con, caminho_analises_result)
    """

    lote = comum.executar_sql_lote(con, f'{comum.CAMINHO_SCRIPTS_ANALISES}/02-ranking/', {
        "04-p-ranking-rec-categoria-mencao-qtd.sql":"qtd"
        ,"04-q-ranking-rec-categoria-mencao-tot-arrecad.sql":"tot-arrecad"
        ,"04-r-ranking-rec-categoria-mencao-avg-arrecad.sql":"avg-arrecad"
        ,"04-s-ranking-rec-categoria-mencao-max-arrecad.sql":"max-arrecad"
        ,"04-t-ranking-rec-categoria-mencao-tx-sucesso.sql":"tx-sucesso"
    })

    comum.gerar_excel_lote(f'{caminho_analises_result}/04-ranking-categoria-mencao-rec.xlsx', lote)
