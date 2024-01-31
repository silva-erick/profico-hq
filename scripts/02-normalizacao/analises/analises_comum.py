import colunas as colunaslib
import pandas as pd
import re

CAMPANHA_AON    = 'aon'
CAMPANHA_FLEX   = 'flex'
CAMPANHA_SUB    = 'sub'

MODALIDADES     = [CAMPANHA_AON, CAMPANHA_FLEX, CAMPANHA_SUB]

TITULOS_MODALIDADES = {
    CAMPANHA_AON    : 'Tudo ou Nada',
    CAMPANHA_FLEX   : 'Flex',
    CAMPANHA_SUB    : 'Recorrente',
}

TITULOS_MODALIDADES_LOWER = {
    CAMPANHA_AON    : 'tudo ou nada',
    CAMPANHA_FLEX   : 'flex',
    CAMPANHA_SUB    : 'recorrente',
}

DFCOL_ANO = f'ano'
DFCOL_TOTAL = f'total'
DFCOL_TOTAL_SUCESSO = f'total_sucesso'
DFCOL_TOTAL_FALHA = f'total_falha'

DFCOL_PARTICIP = f'particip'

DFCOL_TAXA_SUCESSO = f'taxa_sucesso'
DFCOL_ARRECADADO = f'arrecadado'
DFCOL_ARRECADADO_SUCESSO = f'arrecadado_sucesso'

DFCOL_MEDIA_SUCESSO = f'media_sucesso'
DFCOL_STD_SUCESSO = f'std_sucesso'
DFCOL_MIN_SUCESSO = f'min_sucesso'
DFCOL_MAX_SUCESSO = f'max_sucesso'

DFCOL_APOIO_MEDIO = f'apoio_medio'
DFCOL_CONTRIBUICOES = f'contribuicoes'
DFCOL_MEDIA_CONTRIBUICOES = f'media_contribuicoes'



'''
a função de exportação para markdown, disponível no pandas, e que usa a biblioteca tabulate,
não estava com bom comportamento para alinhamento de colunas ou formatação de números para
o pt-br.

até que o comportamento da tabulate melhore, ficou mais simples trabalhar com a localização
padrão (inglês, en-US) e trabalhar na string gerada para garantir:
- separador de milhar
- separador de decimal

também não foi aplicada formatação de números como porcento ou moeda. vamos trabalhar para
isso acontecer.
'''
def formatar_tabelamarkdown_com_milhares(string_com_numeros):
    # Aplicar a formatação com milhares para números com zero ou duas casas decimais
    string_com_numeros = re.sub(r'(\d)(?=(\d{3})+(\.\d{0,2})?\s)', r'\1,', string_com_numeros)

    # Trocar ponto por vírgula e vírgula por ponto para números com zero ou duas casas decimais
    string_com_numeros = re.sub(r'[\+\-]{0,1}(\d{1,3}((,\d{3})+)?(\.\d{0,2})?)', lambda x: x.group().replace('.', 'TEMPORARY_DOT').replace(',', '.').replace('TEMPORARY_DOT', ','), string_com_numeros)

    string_com_numeros = re.sub(r'!(\d+)!', r' \1 ', string_com_numeros)


    return string_com_numeros

def formatar_com_milhares(string_com_numeros):
    string_com_numeros = formatar_numero(string_com_numeros) + ' '
    # Aplicar a formatação com milhares para números com zero ou duas casas decimais
    string_com_numeros = re.sub(r'(\d)(?=(\d{3})+(\.\d{0,2})?\s)', r'\1,', string_com_numeros)

    # Trocar ponto por vírgula e vírgula por ponto para números com zero ou duas casas decimais
    string_com_numeros = re.sub(r'[\+\-]{0,1}(\d{1,3}((,\d{3})+)?(\.\d{0,2})?)', lambda x: x.group().replace('.', 'TEMPORARY_DOT').replace(',', '.').replace('TEMPORARY_DOT', ','), string_com_numeros)

    string_com_numeros = string_com_numeros.replace(' ', '')

    return string_com_numeros


# Função para formatar os números
def formatar_percent(valor):
    if isinstance(valor, str):
        valor_float = float(valor)
    else:
        valor_float = valor
    return f'{100*valor_float:.1f}'

# Função para formatar os números
def formatar_numero(valor):
    if isinstance(valor, str):
        valor_float = float(valor)
    else:
        valor_float = valor
    return f'{valor_float:.2f}'

# Função para formatar os números
def formatar_3casas(valor):
    if isinstance(valor, str):
        valor_float = float(valor)
    else:
        valor_float = valor
    return f'{valor_float:.3f}'

# Função para formatar os números
def formatar_float(valor):
    if isinstance(valor, str):
        valor_float = float(valor)
    else:
        valor_float = valor
    return f'{valor_float:.2f}'

# Função para formatar os números
def formatar_int(valor):
    if isinstance(valor, str):
        valor_int = int(str(round(float(valor), 0)).replace('.00', '').replace('.0', ''))
    elif isinstance(valor, float):
        valor_int = int(str(round(valor, 0)).replace('.00', '').replace('.0', ''))
    else:
        valor_int = int(valor)
    return f'{valor_int}'


# Função para não formatar
def formatar_nada(valor):
    return f'!{valor}!'

# divide dois números, mas se o divisor for zero, apenas retorna zero
def _dividir(dividendo, divisor):
    if divisor == 0:
        return 0
    return dividendo / divisor

# gravar excel formatado
def _gravar_excel_formatado(df_resultado, caminho_arquivo_excel, colunas_formato):
    # Cria um escritor Excel
    with pd.ExcelWriter(caminho_arquivo_excel, engine='xlsxwriter') as writer:
        # Salva o DataFrame no Excel
        df_resultado.to_excel(writer, sheet_name='Sheet1', index=False)

        # Obtém o objeto de planilha
        planilha = writer.sheets['Sheet1']

        # Aplica o formato percentual às colunas
        for coluna, formato_excel in colunas_formato.items():
            if coluna in df_resultado.columns:
                col_idx = df_resultado.columns.get_loc(coluna)
                planilha.set_column(col_idx, col_idx, cell_format=writer.book.add_format(formato_excel))


# calcular o resumo de campanhas por dim e modalidades
def _calcular_resumo_por_dim_modalidade(df, col_dim):

    col_modalidade = colunaslib.COL_GERAL_MODALIDADE

    colunas = [col_modalidade, col_dim]
    df_resultado = df.groupby(colunas).size().reset_index(name='total')

    # estender o df com mais colunas
    for index, row in df_resultado.iterrows():
        dim = row[col_dim]
        total_dim = row['total']
        modalidade = row[col_modalidade]

        campanhas_mod = df[
            (df[col_modalidade] == modalidade)
            ]
        total_mod = len(campanhas_mod)

        campanhas_dim_mod = df[
            (df[col_dim] == dim)
            & (df[col_modalidade] == modalidade)
            ]
        total_dim_mod = len(campanhas_dim_mod)

        if modalidade == 'sub':
            campanhas_dim_mod_sucesso = df[
                (df[col_dim] == dim)
                & (df[col_modalidade] == modalidade)
                & (df[colunaslib.COL_GERAL_TOTAL_CONTRIBUICOES] > 0)
                ]
            total_dim_mod_sucesso = len(campanhas_dim_mod_sucesso)
            valor_dim_mod_sucesso = campanhas_dim_mod_sucesso[colunaslib.COL_GERAL_ARRECADADO_CORRIGIDO].sum()
            std_dim_mod_sucesso = campanhas_dim_mod_sucesso[colunaslib.COL_GERAL_ARRECADADO_CORRIGIDO].std()
            min_dim_mod_sucesso = campanhas_dim_mod_sucesso[colunaslib.COL_GERAL_ARRECADADO_CORRIGIDO].min()
            max_dim_mod_sucesso = campanhas_dim_mod_sucesso[colunaslib.COL_GERAL_ARRECADADO_CORRIGIDO].max()

            contribuicoes = campanhas_dim_mod_sucesso[colunaslib.COL_GERAL_TOTAL_CONTRIBUICOES].sum()
        else:
            campanhas_dim_mod_sucesso = df[
                (df[col_dim] == dim)
                & (df[col_modalidade] == modalidade)
                & (df[colunaslib.COL_GERAL_STATUS] != 'failed')
                ]
            total_dim_mod_sucesso = len(campanhas_dim_mod_sucesso)
            valor_dim_mod_sucesso = campanhas_dim_mod_sucesso[colunaslib.COL_GERAL_ARRECADADO_CORRIGIDO].sum()
            std_dim_mod_sucesso = campanhas_dim_mod_sucesso[colunaslib.COL_GERAL_ARRECADADO_CORRIGIDO].std()
            min_dim_mod_sucesso = campanhas_dim_mod_sucesso[colunaslib.COL_GERAL_ARRECADADO_CORRIGIDO].min()
            max_dim_mod_sucesso = campanhas_dim_mod_sucesso[colunaslib.COL_GERAL_ARRECADADO_CORRIGIDO].max()
            contribuicoes = campanhas_dim_mod_sucesso[colunaslib.COL_GERAL_TOTAL_CONTRIBUICOES].sum()


        df_resultado.at[index, DFCOL_TOTAL] = int(total_dim_mod)
        df_resultado.at[index, DFCOL_TOTAL_SUCESSO] = int(total_dim_mod_sucesso)

        df_resultado.at[index, DFCOL_PARTICIP] = 100 * _dividir(total_dim_mod, total_mod)

        df_resultado.at[index, DFCOL_TAXA_SUCESSO] = 100 * _dividir(total_dim_mod_sucesso, total_dim_mod)

        df_resultado.at[index, DFCOL_ARRECADADO_SUCESSO] = valor_dim_mod_sucesso
        df_resultado.at[index, DFCOL_MEDIA_SUCESSO] = _dividir(valor_dim_mod_sucesso, total_dim_mod_sucesso)
        df_resultado.at[index, DFCOL_STD_SUCESSO] = std_dim_mod_sucesso
        df_resultado.at[index, DFCOL_MIN_SUCESSO] = min_dim_mod_sucesso
        df_resultado.at[index, DFCOL_MAX_SUCESSO] = max_dim_mod_sucesso

        df_resultado.at[index, DFCOL_APOIO_MEDIO] = _dividir(valor_dim_mod_sucesso, contribuicoes)
        df_resultado.at[index, DFCOL_CONTRIBUICOES] = contribuicoes
        df_resultado.at[index, DFCOL_MEDIA_CONTRIBUICOES] = _dividir(contribuicoes, total_dim_mod_sucesso)


    # Preencher NaN com 0 para evitar problemas na divisão
    df_resultado = df_resultado.fillna(0)

    # garantir colunas int64:
    df_resultado[DFCOL_TOTAL] = df_resultado[DFCOL_TOTAL].round().astype('int64')
    df_resultado[DFCOL_TOTAL_SUCESSO] = df_resultado[DFCOL_TOTAL_SUCESSO].round().astype('int64')
    df_resultado[DFCOL_CONTRIBUICOES] = df_resultado[DFCOL_CONTRIBUICOES].round().astype('int64')

    return df_resultado


# calcular série anual de campanhas por dim e modalidades
def _calcular_serie_por_dim_modalidade(df, modalidade, col_dim):

    col_modalidade = colunaslib.COL_GERAL_MODALIDADE
    colunas = ['ano', col_dim]
    df_resultado = df[
        df[col_modalidade] == modalidade
    ].groupby(colunas).size().reset_index(name='total')

    # estender o df com mais colunas
    for index, row in df_resultado.iterrows():
        dim = row[col_dim]
        total_dim = row['total']


        campanhas_mod = df[
            (df[col_modalidade] == modalidade)
            ]
        total_mod = len(campanhas_mod)

        campanhas_dim_mod = df[
            (df[col_dim] == dim)
            & (df[col_modalidade] == modalidade)
            ]
        total_dim_mod = len(campanhas_dim_mod)

        if modalidade == 'sub':
            campanhas_dim_mod_sucesso = df[
                (df[col_dim] == dim)
                & (df[col_modalidade] == modalidade)
                & (df[colunaslib.COL_GERAL_TOTAL_CONTRIBUICOES] > 0)
                ]
            total_dim_mod_sucesso = len(campanhas_dim_mod_sucesso)
            valor_dim_mod_sucesso = campanhas_dim_mod_sucesso[colunaslib.COL_GERAL_ARRECADADO_CORRIGIDO].sum()
            contribuicoes = campanhas_dim_mod_sucesso[colunaslib.COL_GERAL_TOTAL_CONTRIBUICOES].sum()
        else:
            campanhas_dim_mod_sucesso = df[
                (df[col_dim] == dim)
                & (df[col_modalidade] == modalidade)
                & (df[colunaslib.COL_GERAL_STATUS] != 'failed')
                ]
            total_dim_mod_sucesso = len(campanhas_dim_mod_sucesso)
            valor_dim_mod_sucesso = campanhas_dim_mod_sucesso[colunaslib.COL_GERAL_ARRECADADO_CORRIGIDO].sum()
            contribuicoes = campanhas_dim_mod_sucesso[colunaslib.COL_GERAL_TOTAL_CONTRIBUICOES].sum()


        df_resultado.at[index, DFCOL_TOTAL] = int(total_dim_mod)
        df_resultado.at[index, DFCOL_TOTAL_SUCESSO] = int(total_dim_mod_sucesso)

        df_resultado.at[index, DFCOL_TAXA_SUCESSO] = _dividir(total_dim_mod_sucesso, total_dim_mod)

        df_resultado.at[index, DFCOL_ARRECADADO_SUCESSO] = valor_dim_mod_sucesso
        df_resultado.at[index, DFCOL_MEDIA_SUCESSO] = _dividir(valor_dim_mod_sucesso, total_dim_mod_sucesso)

        df_resultado.at[index, DFCOL_APOIO_MEDIO] = _dividir(valor_dim_mod_sucesso, contribuicoes)
        df_resultado.at[index, DFCOL_CONTRIBUICOES] = contribuicoes
        df_resultado.at[index, DFCOL_MEDIA_CONTRIBUICOES] = _dividir(contribuicoes, total_dim_mod_sucesso)

    # Preencher NaN com 0 para evitar problemas na divisão
    df_resultado = df_resultado.fillna(0)

    # garantir colunas int64:
    df_resultado[DFCOL_TOTAL] = df_resultado[DFCOL_TOTAL].round().astype('int64')
    df_resultado[DFCOL_TOTAL_SUCESSO] = df_resultado[DFCOL_TOTAL_SUCESSO].round().astype('int64')
    df_resultado[DFCOL_CONTRIBUICOES] = df_resultado[DFCOL_CONTRIBUICOES].round().astype('int64')

    return df_resultado

def remover_colunas_apoio(dict_df, colunas_apoio):
    res = {}
    for mod in [CAMPANHA_AON, CAMPANHA_FLEX, CAMPANHA_SUB]:
        if mod in dict_df:
            df_temp = dict_df[mod].drop(columns=colunas_apoio)
            res[mod] = df_temp

    return res