import pandas as pd
import analise.comum as comum
import pydot
import duckdb
import formatos
import arquivos
import arquivos_template

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import time


def exportar_visao_geral(args, con, caminho_analises_result):
    """
    def exportar_visao_geral(args, con, caminho_analises_result)
    - executar consultas SQL
    - gerar excel
    - gerar infográfico
    - gerar gráficos
    """

    caminho_scripts = f"{comum.CAMINHO_SCRIPTS_ANALISES}/01-visao-geral"

    lote = comum.executar_sql_lote(con, caminho_scripts, {
        "01-a-visao-geral-modalidade.sql": "modalidade",
        "01-b-visao-geral-plataformas.sql": "plataforma",
        "01-c-visao-geral-uf.sql": "uf",
        "01-d-visao-geral-classificacao-autoria.sql": "classificacao_autoria",
        "01-e-visao-geral-autor.sql": "autor",
        "01-f-visao-geral-categoria-mencao.sql": "categoria"
    })

    comum.gerar_excel_lote(f'{caminho_analises_result}/01-visao-geral.xlsx', lote)

    item_a = lote["01-a-visao-geral-modalidade.sql"]
    item_b = lote["01-b-visao-geral-plataformas.sql"]
    item_c = lote["01-c-visao-geral-uf.sql"]
    item_d = lote["01-d-visao-geral-classificacao-autoria.sql"]
    item_e = lote["01-e-visao-geral-autor.sql"]
    item_f = lote["01-f-visao-geral-categoria-mencao.sql"]

    valores_mapeados = {}
    valores_mapeados['plataformas'] = 'Apoia.se e Catarse'
    analisar_infografico_anos(item_a.df, valores_mapeados)
    analisar_infografico_quantidades(item_a.df, valores_mapeados)
    analisar_infografico_tudo_ou_nada(item_a.df, valores_mapeados)
    analisar_infografico_flex(item_a.df, valores_mapeados)
    analisar_infografico_recorrentes(item_a.df, valores_mapeados)

    grafo_visao_geral = arquivos_template.processar_template(
        f'{caminho_scripts}/infografico.template.dot'
        ,valores_mapeados
        )
    info_dot_geral = pydot.graph_from_dot_data(grafo_visao_geral)
    info_dot_geral[0].write_png(f'{caminho_analises_result}/11-visao-geral.png')


    # gráficos para todas as modalidades
    gerar_graficos(item_a.df, caminho_analises_result, '21-modalidades', 'Modalidades', 'modalidades', 'campanha_modalidade', (10, 6))

    # gráficos para plataformas, por modalidades
    gerar_graficos(item_b.df[
             (item_b.df['campanha_modalidade']=='Tudo ou Nada')
         ], caminho_analises_result, '31-tudo_ou_nada-plataformas', 'Modalidade Tudo ou Nada', 'plataformas', 'campanha_origem', (10, 6))
    gerar_graficos(item_b.df[
             (item_b.df['campanha_modalidade']=='Flex')
         ], caminho_analises_result, '32-flex-plataformas', 'Modalidade Flex', 'plataformas', 'campanha_origem', (10, 6))
    gerar_graficos(item_b.df[
             (item_b.df['campanha_modalidade']=='Recorrente')
         ], caminho_analises_result, '33-recorrente-plataformas', 'Modalidade Recorrente', 'plataformas', 'campanha_origem', (10, 6))

    # gráficos para unidade federativa, por modalidades
    gerar_graficos(item_c.df[
             (item_c.df['campanha_modalidade']=='Tudo ou Nada')
         ], caminho_analises_result, '41-tudo_ou_nada-uf', 'Modalidade Tudo ou Nada', 'unidade federativa', 'uf', (10, 6))
    gerar_graficos(item_c.df[
             (item_c.df['campanha_modalidade']=='Flex')
         ], caminho_analises_result, '42-flex-uf', 'Modalidade Flex', 'unidade federativa', 'uf', (10, 6))
    gerar_graficos(item_c.df[
             (item_c.df['campanha_modalidade']=='Recorrente')
         ], caminho_analises_result, '43-recorrente-uf', 'Modalidade Recorrente', 'unidade federativa', 'uf', (10, 6))

    # gráficos para classificação autoria, por modalidades
    gerar_graficos(item_d.df[
             (item_d.df['campanha_modalidade']=='Tudo ou Nada')
         ], caminho_analises_result, '51-tudo_ou_nada-class_autoria', 'Modalidade Tudo ou Nada', 'classificação de autoria', 'autor_classificacao', (10, 6))
    gerar_graficos(item_d.df[
             (item_d.df['campanha_modalidade']=='Flex')
         ], caminho_analises_result, '52-flex-class_autoria', 'Modalidade Flex', 'classificação de autoria', 'autor_classificacao', (10, 6))
    gerar_graficos(item_d.df[
             (item_d.df['campanha_modalidade']=='Recorrente')
         ], caminho_analises_result, '53-recorrente-class_autoria', 'Modalidade Recorrente', 'classificação de autoria', 'autor_classificacao', (10, 6))

    # gráficos para categoria de conteúdo, por modalidades
    gerar_graficos(item_f.df[
             (item_f.df['campanha_modalidade']=='Tudo ou Nada')
         ], caminho_analises_result, '61-tudo_ou_nada-categ_conteudo', 'Modalidade Tudo ou Nada', 'categoria de conteúdo', 'categoria_mencao', (45, 6))
    gerar_graficos(item_f.df[
             (item_f.df['campanha_modalidade']=='Flex')
         ], caminho_analises_result, '62-flex-categ_conteudo', 'Modalidade Flex', 'categoria de conteúdo', 'categoria_mencao', (45, 6))
    gerar_graficos(item_f.df[
             (item_f.df['campanha_modalidade']=='Recorrente')
         ], caminho_analises_result, '63-recorrente-categ_conteudo', 'Modalidade Recorrente', 'categoria de conteúdo', 'categoria_mencao', (45, 6))


def gerar_graficos(df, caminho_analises_result, prefixo_arquivo, prefixo_titulo, label_eixo_x, eixo_x, figsize):
    """
    gerar gráficos
    """
    comum.gerar_grafico_barras(
        caminho_analises_result
        , f'{prefixo_arquivo}-1-qtd.png'
        , df
        , eixo_x
        , 'qtd'
        , f'{prefixo_titulo}: Quantidade'
        , label_eixo_x
        , 'no. de campanhas'
        , figsize
        )

    comum.gerar_grafico_barras_2series(
        caminho_analises_result
        , f'{prefixo_arquivo}-2-posts.png'
        , df
        , eixo_x
        , 'avg_posts'
        , 'avg_posts_falha'
        , f'{prefixo_titulo}: Média de Posts por Campanha'
        , label_eixo_x
        , 'no. posts (quantidade)'
        , 'média de posts (sucesso)'
        , 'média de posts (falha)'
        , figsize
        )

    comum.gerar_grafico_barras(
        caminho_analises_result
        , f'{prefixo_arquivo}-3-tot_arrecadado.png'
        , df
        , eixo_x
        , 'tot_arrecadado'
        , f'{prefixo_titulo}: Total Arrecadado'
        , label_eixo_x
        , 'valor arrecadado (R$)'
        , figsize
        )

    comum.gerar_grafico_barras(
        caminho_analises_result
        , f'{prefixo_arquivo}-4-avg_arrecadado.png'
        , df
        , eixo_x
        , 'avg_arrecadado'
        , f'{prefixo_titulo}: Arrecadação Média por Campanha'
        , label_eixo_x
        , 'valor arrecadado (R$)'
        , figsize
        )

    comum.gerar_grafico_barras(
        caminho_analises_result
        , f'{prefixo_arquivo}-5-avg_apoio.png'
        , df
        , eixo_x
        , 'avg_apoio'
        , f'{prefixo_titulo}: Apoio Médio por Campanha'
        , label_eixo_x
        , 'no. apoios (quantidade)'
        , figsize
        )

    comum.gerar_grafico_barras(
        caminho_analises_result
        , f'{prefixo_arquivo}-6-txsucesso.png'
        , df
        , eixo_x
        , 'txsucesso'
        , f'{prefixo_titulo}: Taxa de Sucesso'
        , label_eixo_x
        , 'percentual (%)'
        , figsize
        )


def analisar_infografico_anos(df, valores_mapeados):
    """
    def analisar_infografico_anos(df, valores_mapeados)
    analisar anos
    """
    res = duckdb.sql('select min(min_ano) min_ano, max(max_ano) max_ano from df').fetchone()

    valores_mapeados['min_ano'] = str(res[0])
    valores_mapeados['max_ano'] = str(res[1])


def analisar_infografico_quantidades(df, valores_mapeados):
    """
    def analisar_infografico_quantidades(df, valores_mapeados)
    analisar quantidades
    """
    res = duckdb.sql("""
    select  sum(qtd) campanhas_total
            ,sum(qtd) filter ( campanha_modalidade != 'Recorrente' ) campanhas_pontuais_total
            ,sum(qtd) filter ( campanha_modalidade = 'Tudo ou Nada' ) campanhas_aon_total
            ,sum(qtd) filter ( campanha_modalidade = 'Flex' ) campanhas_flex_total
            ,sum(qtd) filter ( campanha_modalidade = 'Recorrente' ) campanhas_sub_total
    from df
    """).fetchall()

    valores_mapeados['campanhas_total'] = str(res[0][0])
    valores_mapeados['campanhas_pontuais_total'] = str(res[0][1])
    valores_mapeados['campanhas_aon_total'] = str(res[0][2])
    valores_mapeados['campanhas_flex_total'] = str(res[0][3])
    valores_mapeados['campanhas_sub_total'] = str(res[0][4])


def analisar_infografico_tudo_ou_nada(df, valores_mapeados):
    """
    def analisar_infografico_tudo_ou_nada(df, valores_mapeados)
    analisar tudo ou nada
    """
    res = duckdb.sql("""
    select  txsucesso
            ,tot_arrecadado
            ,avg_arrecadado
            ,avg_apoio
            ,avg_contribuicoes
            ,tot_contribuicoes
    from    df
    where   campanha_modalidade = 'Tudo ou Nada'
    """).fetchone()

    valores_mapeados['campanhas_aon_sucesso'] = formatos.formatar_num1_ptbr(res[0])
    valores_mapeados['campanhas_aon_total_arrecadado'] = formatos.formatar_num2_ptbr(res[1])
    valores_mapeados['campanhas_aon_arrecadacao_media'] = formatos.formatar_num2_ptbr(res[2])
    valores_mapeados['campanhas_aon_apoio_med'] = formatos.formatar_num2_ptbr(res[3])
    valores_mapeados['campanhas_aon_contr_media'] = formatos.formatar_num1_ptbr(res[4])
    valores_mapeados['campanhas_aon_contr_totais'] = formatos.formatar_num0_ptbr(res[5])


def analisar_infografico_flex(df, valores_mapeados):
    """
    def analisar_infografico_flex(df, valores_mapeados)
    analisar flex
    """
    res = duckdb.sql("""
    select  txsucesso
            ,tot_arrecadado
            ,avg_arrecadado
            ,avg_apoio
            ,avg_contribuicoes
            ,tot_contribuicoes
    from    df
    where   campanha_modalidade = 'Flex'
    """).fetchone()

    valores_mapeados['campanhas_flex_sucesso'] = formatos.formatar_num1_ptbr(res[0])
    valores_mapeados['campanhas_flex_total_arrecadado'] = formatos.formatar_num2_ptbr(res[1])
    valores_mapeados['campanhas_flex_arrecadacao_media'] = formatos.formatar_num2_ptbr(res[2])
    valores_mapeados['campanhas_flex_apoio_med'] = formatos.formatar_num2_ptbr(res[3])
    valores_mapeados['campanhas_flex_contr_media'] = formatos.formatar_num1_ptbr(res[4])
    valores_mapeados['campanhas_flex_contr_totais'] = formatos.formatar_num0_ptbr(res[5])


def analisar_infografico_recorrentes(df, valores_mapeados):
    """
    def analisar_infografico_recorrentes(df, valores_mapeados)
    analisar recorrentes
    """
    res = duckdb.sql("""
    select  txsucesso
            ,tot_arrecadado
            ,avg_arrecadado
            ,avg_apoio
            ,avg_contribuicoes
            ,tot_contribuicoes
    from    df
    where   campanha_modalidade = 'Recorrente'
    """).fetchone()

    valores_mapeados['campanhas_sub_sucesso'] = formatos.formatar_num1_ptbr(res[0])
    valores_mapeados['campanhas_sub_total_arrecadado'] = formatos.formatar_num2_ptbr(res[1])
    valores_mapeados['campanhas_sub_arrecadacao_media'] = formatos.formatar_num2_ptbr(res[2])
    valores_mapeados['campanhas_sub_apoio_med'] = formatos.formatar_num2_ptbr(res[3])
    valores_mapeados['campanhas_sub_contr_media'] = formatos.formatar_num1_ptbr(res[4])
    valores_mapeados['campanhas_sub_contr_totais'] = formatos.formatar_num0_ptbr(res[5])
