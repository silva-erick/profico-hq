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
import analise.ranking as ranking
import analise.serie_ano as serie_ano


def obter_template_infografico(dot_template, df) -> str:
    """
    Obter o template de infográfico
    """

    res = duckdb.sql('select min(min_ano) from df').fetchall()

    tup = duckdb.sql('select min(min_ano) from df').fetchone()[0]


    df_pontuais = df[
        df[analisebase.DFCOL_MODALIDADE] != analisebase.CAMPANHA_SUB
    ]
    df_aon = df[
        df[analisebase.DFCOL_MODALIDADE] == analisebase.CAMPANHA_AON
    ]
    df_flex = df[
        df[analisebase.DFCOL_MODALIDADE] == analisebase.CAMPANHA_FLEX
    ]
    df_sub = df[
        df[analisebase.DFCOL_MODALIDADE] == analisebase.CAMPANHA_SUB
    ]

    valores_substituicao = {}
    valores_substituicao['$(menor-ano)']                        = df[df[analisebase.DFCOL_MENOR_ANO]!=0][analisebase.DFCOL_MENOR_ANO].min()
    valores_substituicao['$(maior-ano)']                        = df[analisebase.DFCOL_MAIOR_ANO].max()
    valores_substituicao['$(campanhas-total)']                  = analisebase.numero_com_separadores(df[analisebase.DFCOL_TOTAL].sum())
    valores_substituicao['$(campanhas-pontuais-total)']         = analisebase.numero_com_separadores(df_pontuais[analisebase.DFCOL_TOTAL].sum())

    valores_substituicao['$(campanhas-aon-total)']              = analisebase.numero_com_separadores(df_aon[analisebase.DFCOL_TOTAL].sum())
    valores_substituicao['$(campanhas-aon-sucesso)']            = analisebase.numero_com_separadores(100*df_aon[analisebase.DFCOL_TAXA_SUCESSO].sum(),1)
    valores_substituicao['$(campanhas-aon-total-arrecadado)']   = analisebase.numero_com_separadores(df_aon[analisebase.DFCOL_ARRECADADO_SUCESSO].sum(), 2)
    valores_substituicao['$(campanhas-aon-arrecadacao-media)']  = analisebase.numero_com_separadores(df_aon[analisebase.DFCOL_ARRECADADO_MED].sum(), 2)
    valores_substituicao['$(campanhas-aon-apoio-med)']          = analisebase.numero_com_separadores(df_aon[analisebase.DFCOL_APOIO_MED].sum(), 2)
    valores_substituicao['$(campanhas-aon-contr-totais)']       = analisebase.numero_com_separadores(df_aon[analisebase.DFCOL_CONTRIBUICOES].sum())
    valores_substituicao['$(campanhas-aon-contr-media)']        = analisebase.numero_com_separadores(df_aon[analisebase.DFCOL_CONTRIBUICOES_MED].sum())

    valores_substituicao['$(campanhas-flex-total)']             = analisebase.numero_com_separadores(df_flex[analisebase.DFCOL_TOTAL].sum())
    valores_substituicao['$(campanhas-flex-sucesso)']           = analisebase.numero_com_separadores(100*df_flex[analisebase.DFCOL_TAXA_SUCESSO].sum(),1)
    valores_substituicao['$(campanhas-flex-total-arrecadado)']  = analisebase.numero_com_separadores(df_flex[analisebase.DFCOL_ARRECADADO_SUCESSO].sum(), 2)
    valores_substituicao['$(campanhas-flex-arrecadacao-media)'] = analisebase.numero_com_separadores(df_flex[analisebase.DFCOL_ARRECADADO_MED].sum(), 2)
    valores_substituicao['$(campanhas-flex-apoio-med)']         = analisebase.numero_com_separadores(df_flex[analisebase.DFCOL_APOIO_MED].sum(), 2)
    valores_substituicao['$(campanhas-flex-contr-totais)']      = analisebase.numero_com_separadores(df_flex[analisebase.DFCOL_CONTRIBUICOES].sum())
    valores_substituicao['$(campanhas-flex-contr-media)']       = analisebase.numero_com_separadores(df_flex[analisebase.DFCOL_CONTRIBUICOES_MED].sum())

    valores_substituicao['$(campanhas-sub-total)']              = analisebase.numero_com_separadores(df_sub[analisebase.DFCOL_TOTAL].sum())
    valores_substituicao['$(campanhas-sub-sucesso)']            = analisebase.numero_com_separadores(100*df_sub[analisebase.DFCOL_TAXA_SUCESSO].sum(),1)
    valores_substituicao['$(campanhas-sub-total-arrecadado)']   = analisebase.numero_com_separadores(df_sub[analisebase.DFCOL_ARRECADADO_SUCESSO].sum(), 2)
    valores_substituicao['$(campanhas-sub-arrecadacao-media)']  = analisebase.numero_com_separadores(df_sub[analisebase.DFCOL_ARRECADADO_MED].sum(), 2)
    valores_substituicao['$(campanhas-sub-apoio-med)']          = analisebase.numero_com_separadores(df_sub[analisebase.DFCOL_APOIO_MED].sum(), 2)
    valores_substituicao['$(campanhas-sub-contr-totais)']       = analisebase.numero_com_separadores(df_sub[analisebase.DFCOL_CONTRIBUICOES].sum())
    valores_substituicao['$(campanhas-sub-contr-media)']        = analisebase.numero_com_separadores(df_sub[analisebase.DFCOL_CONTRIBUICOES_MED].sum())

    resultado = dot_template
    for k, v in valores_substituicao.items():
        if isinstance(v, str):
            valor = v
        else:
            valor = str(v)
        resultado = resultado.replace(k, valor)

    return resultado

async def executar_analise(args):
    """
    coordenar a execução da análise
    """
    p1 = datetime.now()

    caminho_analises = f"{comum.CAMINHO_ANALISES}/{args.ano}"

    caminho_analises_result = f"{caminho_analises}/result"
    caminho_analises_result_visao_geral = f"{caminho_analises_result}/01-visao-geral"
    caminho_analises_result_ranking = f"{caminho_analises_result}/02-ranking"
    caminho_analises_result_series = f"{caminho_analises_result}/03-series"
    caminhos = [
        caminho_analises_result
        , caminho_analises_result_visao_geral
        , caminho_analises_result_ranking
        , caminho_analises_result_series
    ]

    caminho_arq = f"{caminho_analises}/analises_{args.ano}.duckdb"

    for cam in caminhos:
        if not os.path.exists(cam):
            os.mkdir(cam)

    print(f'executar análises (duckdb): {caminho_arq}')
    con = duckdb.connect(caminho_arq)
    
    dados_campanhas.exportar_dados_campanhas(args, con, caminho_analises_result)

    visao_geral.exportar_visao_geral(args, con, caminho_analises_result_visao_geral)

    ranking.exportar_ranking_tdn_uf(args, con, caminho_analises_result_ranking)
    ranking.exportar_ranking_tdn_classificacao_autoria(args, con, caminho_analises_result_ranking)
    ranking.exportar_ranking_tdn_autor(args, con, caminho_analises_result_ranking)    
    ranking.exportar_ranking_tdn_categoria_mencao(args, con, caminho_analises_result_ranking)

    ranking.exportar_ranking_flex_uf(args, con, caminho_analises_result_ranking)
    ranking.exportar_ranking_flex_classificacao_autoria(args, con, caminho_analises_result_ranking)
    ranking.exportar_ranking_flex_autor(args, con, caminho_analises_result_ranking)    
    ranking.exportar_ranking_flex_categoria_mencao(args, con, caminho_analises_result_ranking)

    ranking.exportar_ranking_rec_uf(args, con, caminho_analises_result_ranking)
    ranking.exportar_ranking_rec_classificacao_autoria(args, con, caminho_analises_result_ranking)
    ranking.exportar_ranking_rec_autor(args, con, caminho_analises_result_ranking)    
    ranking.exportar_ranking_rec_categoria_mencao(args, con, caminho_analises_result_ranking)

    serie_ano.exportar_serie_visao_geral(args, con, caminho_analises_result_series)
    serie_ano.exportar_serie_modalidade(args, con, caminho_analises_result_series)
    serie_ano.exportar_serie_uf(args, con, caminho_analises_result_series)
    serie_ano.exportar_serie_classificacao_autoria(args, con, caminho_analises_result_series)
    serie_ano.exportar_serie_categoria_mencao(args, con, caminho_analises_result_series)


    p2 = datetime.now()
    delta = p2-p1
    tempo = delta.seconds + delta.microseconds/1000000

    logs.verbose(args, f'Tempo: {tempo}s')



