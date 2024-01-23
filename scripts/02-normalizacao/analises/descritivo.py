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
    string_com_numeros = re.sub(r'(\d{1,3}((,\d{3})+)?(\.\d{0,2})?)', lambda x: x.group().replace('.', 'TEMPORARY_DOT').replace(',', '.').replace('TEMPORARY_DOT', ','), string_com_numeros)

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
        valor_int = int(valor.replace('.00', ''))
    else:
        valor_int = int(valor)
    return f'{valor_int}'

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
def _calcular_resumo_por_dim_modalidade(df, ano, pasta, arquivo, col_dim, analise_md):
    colunas = ['geral_modalidade', col_dim]
    df_resultado = df.groupby(colunas).size().reset_index(name='total')

    # estender o df com mais colunas
    for index, row in df_resultado.iterrows():
        dim = row[col_dim]
        total_dim = row['total']
        modalidade = row['geral_modalidade']

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
            (df['geral_modalidade'] == modalidade)
            ]
        total_mod = len(campanhas_mod)

        campanhas_dim_mod = df[
            (df[col_dim] == dim)
            & (df['geral_modalidade'] == modalidade)
            ]
        total_dim_mod = len(campanhas_dim_mod)

        if modalidade == 'sub':
            campanhas_dim_mod_sucesso = df[
                (df[col_dim] == dim)
                & (df['geral_modalidade'] == modalidade)
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
                & (df['geral_modalidade'] == modalidade)
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

    colunas.append('total')

    #print(contagem_ocorrencias)

    df_resultado.to_csv(f'{pasta}/{arquivo}_{ano}.csv', index=False, columns=colunas, sep=';', decimal=',', encoding='utf-8-sig')

    caminho_arquivo_excel = f'{pasta}/{arquivo}_{ano}.xlsx'
    formatados = {}
    formatados[f'particip'] = {'num_format': '0.00%'}
    formatados[f'taxa_sucesso'] = {'num_format': '0.00%'}
    formatados[f'valor_sucesso'] = {'num_format': 'R$ #,##0.00'}
    formatados[f'media_sucesso'] = {'num_format': 'R$ #,##0.00'}
    formatados[f'std_sucesso'] = {'num_format': 'R$ #,##0.00'}
    formatados[f'min_sucesso'] = {'num_format': 'R$ #,##0.00'}
    formatados[f'max_sucesso'] = {'num_format': 'R$ #,##0.00'}

    _gravar_excel_formatado(df_resultado, caminho_arquivo_excel, formatados)

    df_formatado = df_resultado.copy()

    for coluna in df_formatado.columns:
        if coluna.startswith('total'):
            df_formatado[coluna] = df_formatado[coluna].map(formatar_int)
        elif coluna =='particip':
            df_formatado[coluna] = df_formatado[coluna].map(formatar_percent)
        elif coluna =='taxa_sucesso':
            df_formatado[coluna] = df_formatado[coluna].map(formatar_percent)
        elif df_formatado[coluna].dtype.name == 'float64':
            df_formatado[coluna] = df_formatado[coluna].map(formatar_numero)

    alinhamento_md = []
    for c in df_resultado.columns:
        d = df_resultado[c].dtype.name
        if d == 'int64':
            alinhamento_md.append('right')
        elif d == 'float64':
            alinhamento_md.append('right')
        else:
            alinhamento_md.append('left')

    mapeamento = {'aon': 'tudo ou nada', 'flex': 'flex', 'sub': 'recorrente'}
    df_formatado['geral_modalidade'] = df_formatado['geral_modalidade'].map(mapeamento)
    df_formatado.rename(columns={'geral_modalidade': 'modalidade'}, inplace=True)

    mk_table = formatar_com_milhares(df_formatado.to_markdown(index=False, disable_numparse=True, colalign=alinhamento_md))

    analise_md.append({arquivo: mk_table})

    return True

# calcular a taxa de sucesso de campanhas por modalidades
def calcular_resumo_por_modalidade(df, ano, pasta, arquivo, analise_md):
    colunas = ['geral_modalidade']
    df_resultado = df.groupby(colunas).size().reset_index(name='total')

    # estender o df com mais colunas
    for index, row in df_resultado.iterrows():
        modalidade = row['geral_modalidade']
        total_mod = row['total']

        col_taxa_sucesso = f'taxa_sucesso'
        col_valor_arrecadado = f'arrecadado'
        col_total_sucesso = f'total_sucesso'
        col_valor_arrecadado_sucesso = f'arrecadado_sucesso'

        col_media_sucesso = f'media_sucesso'
        col_std_sucesso = f'std_sucesso'
        col_min_sucesso = f'min_sucesso'
        col_max_sucesso = f'max_sucesso'

        campanhas_mod = df[
            (df['geral_modalidade'] == modalidade)
            ]
        valor_mod = campanhas_mod['geral_arrecadado_corrigido'].sum()

        if modalidade == 'sub':
            # 'total_mod_mencao' na modalidade com referência à 'menção' com status diferente de falha
            campanhas_mod_sucesso = df[
                (df['geral_modalidade'] == modalidade)
                & (df['geral_total_contribuicoes'] > 0)
                ]
            total_mod_sucesso = len(campanhas_mod_sucesso)
            valor_mod_sucesso = campanhas_mod_sucesso['geral_arrecadado_corrigido'].sum()
            std_mod_sucesso = campanhas_mod_sucesso['geral_arrecadado_corrigido'].std()
            min_mod_sucesso = campanhas_mod_sucesso['geral_arrecadado_corrigido'].min()
            max_mod_sucesso = campanhas_mod_sucesso['geral_arrecadado_corrigido'].max()
        else:
            # 'total_mod_mencao' na modalidade com referência à 'menção' com status diferente de falha
            campanhas_mod_sucesso = df[
                (df['geral_modalidade'] == modalidade)
                & (df['geral_status'] != 'failed')
                ]
            total_mod_sucesso = len(campanhas_mod_sucesso)
            valor_mod_sucesso = campanhas_mod_sucesso['geral_arrecadado_corrigido'].sum()
            std_mod_sucesso = campanhas_mod_sucesso['geral_arrecadado_corrigido'].std()
            min_mod_sucesso = campanhas_mod_sucesso['geral_arrecadado_corrigido'].min()
            max_mod_sucesso = campanhas_mod_sucesso['geral_arrecadado_corrigido'].max()
        
        df_resultado.at[index, col_valor_arrecadado] = valor_mod
        df_resultado.at[index, col_total_sucesso] = int(total_mod_sucesso)
        df_resultado.at[index, col_valor_arrecadado_sucesso] = valor_mod_sucesso
        df_resultado.at[index, col_taxa_sucesso] = _dividir(total_mod_sucesso, total_mod)
        df_resultado.at[index, col_media_sucesso] = _dividir(valor_mod_sucesso, total_mod_sucesso)
        df_resultado.at[index, col_std_sucesso] = std_mod_sucesso
        df_resultado.at[index, col_min_sucesso] = min_mod_sucesso
        df_resultado.at[index, col_max_sucesso] = max_mod_sucesso

    # Preencher NaN com 0 para evitar problemas na divisão
    df_resultado = df_resultado.fillna(0)

    df_resultado.to_csv(f'{pasta}/{arquivo}_{ano}.csv', index=False, sep=';', decimal=',', encoding='utf-8-sig')

    caminho_arquivo_excel = f'{pasta}/{arquivo}_{ano}.xlsx'
    _gravar_excel_formatado(df_resultado, caminho_arquivo_excel, {
        'taxa_sucesso': {'num_format': '0.00%'},
        'arrecadado': {'num_format': 'R$ #,##0.00'},
        'arrecadado_sucesso': {'num_format': 'R$ #,##0.00'},
        'media_sucesso': {'num_format': 'R$ #,##0.00'},
        'std_sucesso': {'num_format': 'R$ #,##0.00'},
        'min_sucesso': {'num_format': 'R$ #,##0.00'},
        'max_sucesso': {'num_format': 'R$ #,##0.00'},
        })

    df_formatado = df_resultado.copy()

    for coluna in df_formatado.columns:
        if coluna.startswith('total'):
            df_formatado[coluna] = df_formatado[coluna].map(formatar_int)
        elif coluna =='particip':
            df_formatado[coluna] = df_formatado[coluna].map(formatar_percent)
        elif coluna =='taxa_sucesso':
            df_formatado[coluna] = df_formatado[coluna].map(formatar_percent)
        elif df_formatado[coluna].dtype.name == 'float64':
            df_formatado[coluna] = df_formatado[coluna].map(formatar_numero)

    
    alinhamento_md = []
    for c in df_resultado.columns:
        d = df_resultado[c].dtype.name
        if d == 'int64':
            alinhamento_md.append('right')
        elif d == 'float64':
            alinhamento_md.append('right')
        else:
            alinhamento_md.append('left')

    mapeamento = {'aon': 'tudo ou nada', 'flex': 'flex', 'sub': 'recorrente'}
    df_formatado['geral_modalidade'] = df_formatado['geral_modalidade'].map(mapeamento)
    df_formatado.rename(columns={'geral_modalidade': 'modalidade'}, inplace=True)

    mk_table = formatar_com_milhares(df_formatado.to_markdown(index=False, disable_numparse=True, colalign=alinhamento_md))

    analise_md.append({arquivo: mk_table})

    return True

# calcular o resumo de campanhas por origem e modalidades
def calcular_resumo_por_origem_modalidade(df, ano, pasta, arquivo, analise_md):
    return _calcular_resumo_por_dim_modalidade(df, ano, pasta, arquivo, 'origem', analise_md)

# calcular o resumo de campanhas por uf_br
def calcular_resumo_por_ufbr(df, ano, pasta, arquivo, analise_md):
    return _calcular_resumo_por_dim_modalidade(df, ano, pasta, arquivo, 'geral_uf_br', analise_md)

# calcular o resumo de campanhas por gênero
def calcular_resumo_por_genero(df, ano, pasta, arquivo, analise_md):
    return _calcular_resumo_por_dim_modalidade(df, ano, pasta, arquivo, 'autoria_classificacao', analise_md)

# calcular o resumo de campanhas por autoria e seus respectivos status
def calcular_resumo_por_autoria(df, ano, pasta, arquivo, analise_md):
    return _calcular_resumo_por_dim_modalidade(df, ano, pasta, arquivo, 'autoria_nome_publico', analise_md)

# return _calcular_resumo_por_dim_modalidade(df[(df[col] == True)], ano, pasta, arquivo, col, analise_md)
# calcular o resumo de menção de acordo com a modalidade das campanhas
def calcular_resumo_por_mencoes_angelo_agostini(df, ano, pasta, arquivo, analise_md):
    col =  'mencoes_angelo_agostini'
    return _calcular_resumo_por_dim_modalidade(df, ano, pasta, arquivo, col, analise_md)

# calcular o resumo de menção de acordo com a modalidade das campanhas
def calcular_resumo_por_mencoes_ccxp(df, ano, pasta, arquivo, analise_md):
    col =  'mencoes_ccxp'
    return _calcular_resumo_por_dim_modalidade(df, ano, pasta, arquivo, col, analise_md)

# calcular o resumo de menção de acordo com a modalidade das campanhas
def calcular_resumo_por_mencoes_disputa(df, ano, pasta, arquivo, analise_md):
    col =  'mencoes_disputa'
    return _calcular_resumo_por_dim_modalidade(df, ano, pasta, arquivo, col, analise_md)

# calcular o resumo de menção de acordo com a modalidade das campanhas
def calcular_resumo_por_mencoes_erotismo(df, ano, pasta, arquivo, analise_md):
    col =  'mencoes_erotismo'
    return _calcular_resumo_por_dim_modalidade(df, ano, pasta, arquivo, col, analise_md)

# calcular o resumo de menção de acordo com a modalidade das campanhas
def calcular_resumo_por_mencoes_fantasia(df, ano, pasta, arquivo, analise_md):
    col =  'mencoes_fantasia'
    return _calcular_resumo_por_dim_modalidade(df, ano, pasta, arquivo, col, analise_md)

# calcular o resumo de menção de acordo com a modalidade das campanhas
def calcular_resumo_por_mencoes_ficcao_cientifica(df, ano, pasta, arquivo, analise_md):
    col =  'mencoes_ficcao_cientifica'
    return _calcular_resumo_por_dim_modalidade(df, ano, pasta, arquivo, col, analise_md)

# calcular o resumo de menção de acordo com a modalidade das campanhas
def calcular_resumo_por_mencoes_fiq(df, ano, pasta, arquivo, analise_md):
    col =  'mencoes_fiq'
    return _calcular_resumo_por_dim_modalidade(df, ano, pasta, arquivo, col, analise_md)

# calcular o resumo de menção de acordo com a modalidade das campanhas
def calcular_resumo_por_mencoes_folclore(df, ano, pasta, arquivo, analise_md):
    col =  'mencoes_folclore'
    return _calcular_resumo_por_dim_modalidade(df, ano, pasta, arquivo, col, analise_md)

# calcular o resumo de menção de acordo com a modalidade das campanhas
def calcular_resumo_por_mencoes_herois(df, ano, pasta, arquivo, analise_md):
    col =  'mencoes_herois'
    return _calcular_resumo_por_dim_modalidade(df, ano, pasta, arquivo, col, analise_md)

# calcular o resumo de menção de acordo com a modalidade das campanhas
def calcular_resumo_por_mencoes_hqmix(df, ano, pasta, arquivo, analise_md):
    col =  'mencoes_hqmix'
    return _calcular_resumo_por_dim_modalidade(df, ano, pasta, arquivo, col, analise_md)

# calcular o resumo de menção de acordo com a modalidade das campanhas
def calcular_resumo_por_mencoes_humor(df, ano, pasta, arquivo, analise_md):
    col =  'mencoes_humor'
    return _calcular_resumo_por_dim_modalidade(df, ano, pasta, arquivo, col, analise_md)

# calcular o resumo de menção de acordo com a modalidade das campanhas
def calcular_resumo_por_mencoes_jogos(df, ano, pasta, arquivo, analise_md):
    col =  'mencoes_jogos'
    return _calcular_resumo_por_dim_modalidade(df, ano, pasta, arquivo, col, analise_md)

# calcular o resumo de menção de acordo com a modalidade das campanhas
def calcular_resumo_por_mencoes_lgbtqiamais(df, ano, pasta, arquivo, analise_md):
    col =  'mencoes_lgbtqiamais'
    return _calcular_resumo_por_dim_modalidade(df, ano, pasta, arquivo, col, analise_md)

# calcular o resumo de menção de acordo com a modalidade das campanhas
def calcular_resumo_por_mencoes_midia_independente(df, ano, pasta, arquivo, analise_md):
    col =  'mencoes_midia_independente'
    return _calcular_resumo_por_dim_modalidade(df, ano, pasta, arquivo, col, analise_md)

# calcular o resumo de menção de acordo com a modalidade das campanhas
def calcular_resumo_por_mencoes_politica(df, ano, pasta, arquivo, analise_md):
    col =  'mencoes_politica'
    return _calcular_resumo_por_dim_modalidade(df, ano, pasta, arquivo, col, analise_md)

# calcular o resumo de menção de acordo com a modalidade das campanhas
def calcular_resumo_por_mencoes_questoes_genero(df, ano, pasta, arquivo, analise_md):
    col =  'mencoes_questoes_genero'
    return _calcular_resumo_por_dim_modalidade(df, ano, pasta, arquivo, col, analise_md)

# calcular o resumo de menção de acordo com a modalidade das campanhas
def calcular_resumo_por_mencoes_religiosidade(df, ano, pasta, arquivo, analise_md):
    col =  'mencoes_religiosidade'
    return _calcular_resumo_por_dim_modalidade(df, ano, pasta, arquivo, col, analise_md)

# calcular o resumo de menção de acordo com a modalidade das campanhas
def calcular_resumo_por_mencoes_saloes_humor(df, ano, pasta, arquivo, analise_md):
    col =  'mencoes_saloes_humor'
    return _calcular_resumo_por_dim_modalidade(df, ano, pasta, arquivo, col, analise_md)

# calcular o resumo de menção de acordo com a modalidade das campanhas
def calcular_resumo_por_mencoes_terror(df, ano, pasta, arquivo, analise_md):
    col =  'mencoes_terror'
    return _calcular_resumo_por_dim_modalidade(df, ano, pasta, arquivo, col, analise_md)

# calcular o resumo de menção de acordo com a modalidade das campanhas
def calcular_resumo_por_mencoes_webformatos(df, ano, pasta, arquivo, analise_md):
    col =  'mencoes_webformatos'
    return _calcular_resumo_por_dim_modalidade(df, ano, pasta, arquivo, col, analise_md)

# calcular o resumo de menção de acordo com a modalidade das campanhas
def calcular_resumo_por_mencoes_zine(df, ano, pasta, arquivo, analise_md):
    col =  'mencoes_zine'
    return _calcular_resumo_por_dim_modalidade(df, ano, pasta, arquivo, col, analise_md)
