import pandas as pd
import analise.comum as comum
import arquivos

def exportar_dados_campanhas(args, con, caminho_analises_result):
    """
    exportar os dados gerais da campanha:
    - lista de campanhas
    - origem-dados
    - status-campanha
    - classificação-autoria
    - modalidade-campanha
    - categoria-menção
    - autoria
    - município
    - unidade-federativa
    """

    lote = comum.executar_sql_lote(con, f'{comum.CAMINHO_SCRIPTS_ANALISES}/00-campanhas/', {
        "00-lista-campanhas.sql":"campanhas"
        ,"01-origem-dados.sql":"origem-dados"
        ,"02-status-campanha.sql":"status-campanha"
        ,"03-classificacao-autor.sql":"classificação-autoria"
        ,"04-modalidade-campanha.sql":"modalidade-campanha"
        ,"05-categoria.sql":"categoria-menção"
        ,"06-autoria.sql":"autoria"
        ,"07-municipio.sql":"município"
        ,"08-unidade-federativa.sql":"unidade-federativa"
    })

    comum.gerar_excel_lote(args, f'{caminho_analises_result}', '00-lista-campanhas.xlsx', lote)
