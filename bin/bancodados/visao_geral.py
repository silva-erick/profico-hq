import pandas as pd
import bancodados.comum as comum
import pydot
import duckdb
import formatos


'''
def exportar_visao_geral(args, con, caminho_analises_result)
'''
def exportar_visao_geral(args, con, caminho_analises_result):

    caminho_scripts = f"{comum.CAMINHO_SCRIPTS_ANALISES}/01-visao-geral"

    sql = comum.ler_arquivo(f'{caminho_scripts}/01-a-visao-geral-modalidade.sql')
    res = con.sql(sql)
    dfa = res.to_df()

    sql = comum.ler_arquivo(f'{caminho_scripts}/01-b-visao-geral-plataformas.sql')
    res = con.sql(sql)
    dfb = res.to_df()

    sql = comum.ler_arquivo(f'{caminho_scripts}/01-c-visao-geral-uf.sql')
    res = con.sql(sql)
    dfc = res.to_df()

    sql = comum.ler_arquivo(f'{caminho_scripts}/01-d-visao-geral-classificacao-autoria.sql')
    res = con.sql(sql)
    dfd = res.to_df()

    sql = comum.ler_arquivo(f'{caminho_scripts}/01-e-visao-geral-autor.sql')
    res = con.sql(sql)
    dfe = res.to_df()

    sql = comum.ler_arquivo(f'{caminho_scripts}/01-f-visao-geral-categoria-mencao.sql')
    res = con.sql(sql)
    dff = res.to_df()

    with pd.ExcelWriter(f'{caminho_analises_result}/01-visao-geral.xlsx') as writer:  
        dfa.to_excel(writer, sheet_name='modalidade', index=False)
        dfb.to_excel(writer, sheet_name='plataforma', index=False)
        dfc.to_excel(writer, sheet_name='uf', index=False)
        dfd.to_excel(writer, sheet_name='classificacao_autoria', index=False)
        dfe.to_excel(writer, sheet_name='autoria', index=False)
        dff.to_excel(writer, sheet_name='categoria', index=False)

    valores_mapeados = {}
    valores_mapeados['plataformas'] = 'Apoia.se e Catarse'
    analisar_anos(dfa, valores_mapeados)
    analisar_quantidades(dfa, valores_mapeados)
    analisar_tudo_ou_nada(dfa, valores_mapeados)
    analisar_flex(dfa, valores_mapeados)
    analisar_recorrentes(dfa, valores_mapeados)

    grafo_visao_geral = comum.processar_template(
        f'{caminho_scripts}/infografico.template.dot'
        ,valores_mapeados
        )
    info_dot_geral = pydot.graph_from_dot_data(grafo_visao_geral)
    info_dot_geral[0].write_png(f'{caminho_analises_result}/11-visao-geral.png')

def analisar_anos(df, valores_mapeados):
    res = duckdb.sql('select min(min_ano) min_ano, max(max_ano) max_ano from df').fetchone()

    valores_mapeados['min_ano'] = str(res[0])
    valores_mapeados['max_ano'] = str(res[1])

def analisar_quantidades(df, valores_mapeados):
    res = duckdb.sql('''
    select  sum(qtd) campanhas_total
            ,sum(qtd) filter ( campanha_modalidade != 'Recorrente' ) campanhas_pontuais_total
            ,sum(qtd) filter ( campanha_modalidade = 'Tudo ou Nada' ) campanhas_aon_total
            ,sum(qtd) filter ( campanha_modalidade = 'Flex' ) campanhas_flex_total
            ,sum(qtd) filter ( campanha_modalidade = 'Recorrente' ) campanhas_sub_total
    from df
    ''').fetchall()

    valores_mapeados['campanhas_total'] = str(res[0][0])
    valores_mapeados['campanhas_pontuais_total'] = str(res[0][1])
    valores_mapeados['campanhas_aon_total'] = str(res[0][2])
    valores_mapeados['campanhas_flex_total'] = str(res[0][3])
    valores_mapeados['campanhas_sub_total'] = str(res[0][4])

def analisar_tudo_ou_nada(df, valores_mapeados):
    res = duckdb.sql('''
    select  txsucesso
            ,tot_arrecadado
            ,avg_arrecadado
            ,avg_apoio
            ,avg_contribuicoes
            ,tot_contribuicoes
    from    df
    where   campanha_modalidade = 'Tudo ou Nada'
    ''').fetchone()

    valores_mapeados['campanhas_aon_sucesso'] = formatos.formatar_num1_ptbr(res[0])
    valores_mapeados['campanhas_aon_total_arrecadado'] = formatos.formatar_num2_ptbr(res[1])
    valores_mapeados['campanhas_aon_arrecadacao_media'] = formatos.formatar_num2_ptbr(res[2])
    valores_mapeados['campanhas_aon_apoio_med'] = formatos.formatar_num2_ptbr(res[3])
    valores_mapeados['campanhas_aon_contr_media'] = formatos.formatar_num1_ptbr(res[4])
    valores_mapeados['campanhas_aon_contr_totais'] = formatos.formatar_num0_ptbr(res[5])


def analisar_flex(df, valores_mapeados):
    res = duckdb.sql('''
    select  txsucesso
            ,tot_arrecadado
            ,avg_arrecadado
            ,avg_apoio
            ,avg_contribuicoes
            ,tot_contribuicoes
    from    df
    where   campanha_modalidade = 'Flex'
    ''').fetchone()

    valores_mapeados['campanhas_flex_sucesso'] = formatos.formatar_num1_ptbr(res[0])
    valores_mapeados['campanhas_flex_total_arrecadado'] = formatos.formatar_num2_ptbr(res[1])
    valores_mapeados['campanhas_flex_arrecadacao_media'] = formatos.formatar_num2_ptbr(res[2])
    valores_mapeados['campanhas_flex_apoio_med'] = formatos.formatar_num2_ptbr(res[3])
    valores_mapeados['campanhas_flex_contr_media'] = formatos.formatar_num1_ptbr(res[4])
    valores_mapeados['campanhas_flex_contr_totais'] = formatos.formatar_num0_ptbr(res[5])



def analisar_recorrentes(df, valores_mapeados):
    res = duckdb.sql('''
    select  txsucesso
            ,tot_arrecadado
            ,avg_arrecadado
            ,avg_apoio
            ,avg_contribuicoes
            ,tot_contribuicoes
    from    df
    where   campanha_modalidade = 'Recorrente'
    ''').fetchone()

    valores_mapeados['campanhas_sub_sucesso'] = formatos.formatar_num1_ptbr(res[0])
    valores_mapeados['campanhas_sub_total_arrecadado'] = formatos.formatar_num2_ptbr(res[1])
    valores_mapeados['campanhas_sub_arrecadacao_media'] = formatos.formatar_num2_ptbr(res[2])
    valores_mapeados['campanhas_sub_apoio_med'] = formatos.formatar_num2_ptbr(res[3])
    valores_mapeados['campanhas_sub_contr_media'] = formatos.formatar_num1_ptbr(res[4])
    valores_mapeados['campanhas_sub_contr_totais'] = formatos.formatar_num0_ptbr(res[5])
