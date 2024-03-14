import analises.analise_lib as analisebase
import colunas as colunaslib
import pandas as pd
import os


CAMINHO_CSV = "../../dados/csv"
CAMINHO_TEMPLATE = f"templates"
CAMINHO_TEMPLATE_DESCRITIVO = f"{CAMINHO_TEMPLATE}/temporal"

class CoordenadorAnaliseTemporal(analisebase.AnaliseInterface):

    """
    Coordenar a execução da análise temporal
    """
    def executar(self, df, ano_referencia) -> bool:

        calc = CalculosTemporais()
        print(f'> análise temporal')
        print(f'\t. calcular séries: ', end='')
        resultado = calc.executar(df)
        print(f'{resultado}')

        if resultado:

            pasta_md = analisebase.garantir_pasta(f'{CAMINHO_CSV}/{ano_referencia}/analise_temporal')
            pasta_dados = analisebase.garantir_pasta(f'{CAMINHO_CSV}/{ano_referencia}/analise_temporal/dados')
            pasta_img = analisebase.garantir_pasta(f'{CAMINHO_CSV}/{ano_referencia}/analise_temporal/img')

            # resultado = (
            #     self._gerar_infografico(pasta_md, pasta_img, calc.df_resumo_mod, calc.df_resumo_mod_plataforma)
            #     and self._calcular_modalidades(calc, pasta_md, pasta_img, pasta_dados)
            #     and self._gerar_readme(calc, pasta_md)
            # )

        return resultado

class CalculosTemporais(analisebase.AnaliseInterface):

    """
    Executar a análise temporal
    """
    def executar(self, df_completo) -> bool:
        resultado = True

        return resultado
