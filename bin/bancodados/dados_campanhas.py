import pandas as pd
import bancodados.comum as comum

'''
def exportar_dados_campanhas(args, con)
'''
def exportar_dados_campanhas(args, con, caminho_analises_result):
    sql = comum.ler_arquivo(f'{comum.CAMINHO_SCRIPTS_ANALISES}/00-campanhas/00-lista-campanhas.sql')
    res = con.sql(sql)
    dfa = res.to_df()

    sql = comum.ler_arquivo(f'{comum.CAMINHO_SCRIPTS_ANALISES}/00-campanhas/01-origem-dados.sql')
    res = con.sql(sql)
    dfb = res.to_df()

    sql = comum.ler_arquivo(f'{comum.CAMINHO_SCRIPTS_ANALISES}/00-campanhas/02-status-campanha.sql')
    res = con.sql(sql)
    dfc = res.to_df()

    sql = comum.ler_arquivo(f'{comum.CAMINHO_SCRIPTS_ANALISES}/00-campanhas/03-classificacao-autor.sql')
    res = con.sql(sql)
    dfd = res.to_df()

    sql = comum.ler_arquivo(f'{comum.CAMINHO_SCRIPTS_ANALISES}/00-campanhas/04-modalidade-campanha.sql')
    res = con.sql(sql)
    dfe = res.to_df()

    sql = comum.ler_arquivo(f'{comum.CAMINHO_SCRIPTS_ANALISES}/00-campanhas/05-categoria-mencao.sql')
    res = con.sql(sql)
    dff = res.to_df()

    sql = comum.ler_arquivo(f'{comum.CAMINHO_SCRIPTS_ANALISES}/00-campanhas/06-autoria.sql')
    res = con.sql(sql)
    dfg = res.to_df()

    sql = comum.ler_arquivo(f'{comum.CAMINHO_SCRIPTS_ANALISES}/00-campanhas/07-municipio.sql')
    res = con.sql(sql)
    dfh = res.to_df()

    sql = comum.ler_arquivo(f'{comum.CAMINHO_SCRIPTS_ANALISES}/00-campanhas/08-unidade-federativa.sql')
    res = con.sql(sql)
    dfi = res.to_df()

    with pd.ExcelWriter(f'{caminho_analises_result}/00-lista-campanhas.xlsx') as writer:  
        dfa.to_excel(writer, sheet_name='campanhas', index=False)
        dfb.to_excel(writer, sheet_name='origem-dados', index=False)
        dfc.to_excel(writer, sheet_name='status-campanha', index=False)
        dfd.to_excel(writer, sheet_name='classificação-autoria', index=False)
        dfe.to_excel(writer, sheet_name='modalidade-campanha', index=False)
        dff.to_excel(writer, sheet_name='categoria-menção', index=False)
        dfg.to_excel(writer, sheet_name='autoria', index=False)
        dfh.to_excel(writer, sheet_name='município', index=False)
        dfi.to_excel(writer, sheet_name='unidade-federativa', index=False)
