import analises.analise_lib as analisebase
import colunas as colunaslib
import pandas as pd
import os


CAMINHO_CSV = "../../dados/csv"
CAMINHO_TEMPLATE = f"templates"
CAMINHO_TEMPLATE_DESCRITIVO = f"{CAMINHO_TEMPLATE}/notaveis"

class CoordenadorAnaliseNotaveis(analisebase.AnaliseInterface):

    """
    Coordenar a execução da análise notáveis
    """
    def executar(self, df, ano_referencia) -> bool:

        calc = CalculosPontosNotaveis()
        print(f'> análise notáveis')
        print(f'\t. construir rankings: ', end='')
        resultado = calc.executar(df)
        print(f'{resultado}')

        if resultado:

            pasta_md = analisebase.garantir_pasta(f'{CAMINHO_CSV}/{ano_referencia}/analise_notaveis')
            pasta_dados = analisebase.garantir_pasta(f'{CAMINHO_CSV}/{ano_referencia}/analise_notaveis/dados')
            pasta_img = analisebase.garantir_pasta(f'{CAMINHO_CSV}/{ano_referencia}/analise_notaveis/img')

            # resultado = (
            #     self._gerar_infografico(pasta_md, pasta_img, calc.df_resumo_mod, calc.df_resumo_mod_plataforma)
            #     and self._calcular_modalidades(calc, pasta_md, pasta_img, pasta_dados)
            #     and self._gerar_readme(calc, pasta_md)
            # )

        return resultado

class CalculosPontosNotaveis(analisebase.AnaliseInterface):

    """
    Executar a análise notáveis
    """
    def executar(self, df_completo) -> bool:
        resultado = True

        return resultado
