import pandas as pd
import bancodados.comum as comum

'''
def exportar_dados_campanhas(args, con)
'''
def exportar_dados_campanhas(args, con, caminho_analises_result):
    sql = comum.ler_arquivo(f'{comum.CAMINHO_SCRIPTS_ANALISES}/00-campanhas/00-lista-campanhas.sql')
    res = con.sql(sql)
    df = res.to_df()
    df.to_excel(f'{caminho_analises_result}/00-lista-campanhas.xlsx', index=False)
