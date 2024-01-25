import pandas as pd
import re

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
def formatar_com_milhares(string_com_numeros):
    # Aplicar a formatação com milhares para números com zero ou duas casas decimais
    string_com_numeros = re.sub(r'(\d)(?=(\d{3})+(\.\d{0,2})?\s)', r'\1,', string_com_numeros)

    # Trocar ponto por vírgula e vírgula por ponto para números com zero ou duas casas decimais
    string_com_numeros = re.sub(r'[\+\-]{0,1}(\d{1,3}((,\d{3})+)?(\.\d{0,2})?)', lambda x: x.group().replace('.', 'TEMPORARY_DOT').replace(',', '.').replace('TEMPORARY_DOT', ','), string_com_numeros)

    string_com_numeros = re.sub(r'!(\d+)!', r' \1 ', string_com_numeros)


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
        valor_int = int(valor.replace('.00', '').replace('.0', ''))
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

    col_modalidade = 'geral_modalidade'

    colunas = [col_modalidade, col_dim]
    df_resultado = df.groupby(colunas).size().reset_index(name='total')

    # estender o df com mais colunas
    for index, row in df_resultado.iterrows():
        dim = row[col_dim]
        total_dim = row['total']
        modalidade = row[col_modalidade]

        col_total = f'total'
        col_total_sucesso = f'total_sucesso'
        col_total_falha = f'total_falha'

        col_particip = f'particip'

        col_taxa_sucesso = f'taxa_sucesso'
        col_valor_mod_sucesso = f'valor_sucesso'

        col_media_sucesso = f'media_sucesso'
        col_std_sucesso = f'std_sucesso'
        col_min_sucesso = f'min_sucesso'
        col_max_sucesso = f'max_sucesso'

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
                & (df['geral_total_contribuicoes'] > 0)
                ]
            total_dim_mod_sucesso = len(campanhas_dim_mod_sucesso)
            valor_dim_mod_sucesso = campanhas_dim_mod_sucesso['geral_arrecadado_corrigido'].sum()
            std_dim_mod_sucesso = campanhas_dim_mod_sucesso['geral_arrecadado_corrigido'].std()
            min_dim_mod_sucesso = campanhas_dim_mod_sucesso['geral_arrecadado_corrigido'].min()
            max_dim_mod_sucesso = campanhas_dim_mod_sucesso['geral_arrecadado_corrigido'].max()
        else:
            campanhas_dim_mod_sucesso = df[
                (df[col_dim] == dim)
                & (df[col_modalidade] == modalidade)
                & (df['geral_status'] != 'failed')
                ]
            total_dim_mod_sucesso = len(campanhas_dim_mod_sucesso)
            valor_dim_mod_sucesso = campanhas_dim_mod_sucesso['geral_arrecadado_corrigido'].sum()
            std_dim_mod_sucesso = campanhas_dim_mod_sucesso['geral_arrecadado_corrigido'].std()
            min_dim_mod_sucesso = campanhas_dim_mod_sucesso['geral_arrecadado_corrigido'].min()
            max_dim_mod_sucesso = campanhas_dim_mod_sucesso['geral_arrecadado_corrigido'].max()


        df_resultado.at[index, col_total] = int(total_dim_mod)
        df_resultado.at[index, col_total_sucesso] = int(total_dim_mod_sucesso)

        df_resultado.at[index, col_particip] = _dividir(total_dim_mod, total_mod)

        df_resultado.at[index, col_taxa_sucesso] = _dividir(total_dim_mod_sucesso, total_dim_mod)

        df_resultado.at[index, col_valor_mod_sucesso] = valor_dim_mod_sucesso
        df_resultado.at[index, col_media_sucesso] = _dividir(valor_dim_mod_sucesso, total_dim_mod_sucesso)
        df_resultado.at[index, col_std_sucesso] = std_dim_mod_sucesso
        df_resultado.at[index, col_min_sucesso] = min_dim_mod_sucesso
        df_resultado.at[index, col_max_sucesso] = max_dim_mod_sucesso


    # Preencher NaN com 0 para evitar problemas na divisão
    df_resultado = df_resultado.fillna(0)

    return df_resultado


# calcular série anual de campanhas por dim e modalidades
def _calcular_serie_por_dim_modalidade(df, modalidade, col_dim):

    col_modalidade = 'geral_modalidade'
    colunas = ['ano', col_dim]
    df_resultado = df[
        df[col_modalidade] == modalidade
    ].groupby(colunas).size().reset_index(name='total')

    # estender o df com mais colunas
    for index, row in df_resultado.iterrows():
        dim = row[col_dim]
        total_dim = row['total']

        col_total = f'total'
        col_total_sucesso = f'total_sucesso'

        col_taxa_sucesso = f'taxa_sucesso'
        col_valor_mod_sucesso = f'valor_sucesso'
        col_media_sucesso = f'media_sucesso'

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
                & (df['geral_total_contribuicoes'] > 0)
                ]
            total_dim_mod_sucesso = len(campanhas_dim_mod_sucesso)
            valor_dim_mod_sucesso = campanhas_dim_mod_sucesso['geral_arrecadado_corrigido'].sum()
        else:
            campanhas_dim_mod_sucesso = df[
                (df[col_dim] == dim)
                & (df[col_modalidade] == modalidade)
                & (df['geral_status'] != 'failed')
                ]
            total_dim_mod_sucesso = len(campanhas_dim_mod_sucesso)
            valor_dim_mod_sucesso = campanhas_dim_mod_sucesso['geral_arrecadado_corrigido'].sum()


        df_resultado.at[index, col_total] = int(total_dim_mod)
        df_resultado.at[index, col_total_sucesso] = int(total_dim_mod_sucesso)

        df_resultado.at[index, col_taxa_sucesso] = _dividir(total_dim_mod_sucesso, total_dim_mod)

        df_resultado.at[index, col_valor_mod_sucesso] = valor_dim_mod_sucesso
        df_resultado.at[index, col_media_sucesso] = _dividir(valor_dim_mod_sucesso, total_dim_mod_sucesso)

    # Preencher NaN com 0 para evitar problemas na divisão
    df_resultado = df_resultado.fillna(0)

    return df_resultado
