import pandas as pd
import analises.analises_comum as comum

# gerar o resumo de campanhas por dim e modalidades
def _gerar_resumo_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col_dim, analise_md):

    df_resultado = comum._calcular_resumo_por_dim_modalidade(df, col_dim)

    colunas = df_resultado.columns

    df_resultado.to_csv(f'{pasta_dados}/{arquivo}_{ano}.csv', index=False, columns=colunas, sep=';', decimal=',', encoding='utf-8-sig')

    caminho_arquivo_excel = f'{pasta_dados}/{arquivo}_{ano}.xlsx'
    formatados = {}
    formatados[f'particip'] = {'num_format': '0.00%'}
    formatados[f'taxa_sucesso'] = {'num_format': '0.00%'}
    formatados[f'valor_sucesso'] = {'num_format': 'R$ #,##0.00'}
    formatados[f'media_sucesso'] = {'num_format': 'R$ #,##0.00'}
    formatados[f'std_sucesso'] = {'num_format': 'R$ #,##0.00'}
    formatados[f'min_sucesso'] = {'num_format': 'R$ #,##0.00'}
    formatados[f'max_sucesso'] = {'num_format': 'R$ #,##0.00'}

    comum._gravar_excel_formatado(df_resultado, caminho_arquivo_excel, formatados)

    df_formatado = df_resultado.copy()

    for coluna in df_formatado.columns:
        if coluna.startswith('total'):
            df_formatado[coluna] = df_formatado[coluna].map(comum.formatar_int)
        elif coluna =='particip':
            df_formatado[coluna] = df_formatado[coluna].map(comum.formatar_percent)
        elif coluna =='taxa_sucesso':
            df_formatado[coluna] = df_formatado[coluna].map(comum.formatar_percent)
        elif df_formatado[coluna].dtype.name == 'float64':
            df_formatado[coluna] = df_formatado[coluna].map(comum.formatar_numero)

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

    mk_table = comum.formatar_com_milhares(df_formatado.to_markdown(index=False, disable_numparse=True, colalign=alinhamento_md))

    with open(f'{pasta_md}/{arquivo}.md', 'w', encoding='utf8') as md_descritivo:
        md_descritivo.write(f'{template.replace("$(nome_dimensao)", titulo)}')

        md_descritivo.write('\n')
        md_descritivo.write(f'{mk_table}')
        md_descritivo.write('\n')

        md_descritivo.close()


    analise_md.append({arquivo: mk_table})

    return True

# calcular a taxa de sucesso de campanhas por modalidades
def gerar_resumo_por_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
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
        df_resultado.at[index, col_taxa_sucesso] = comum._dividir(total_mod_sucesso, total_mod)
        df_resultado.at[index, col_media_sucesso] = comum._dividir(valor_mod_sucesso, total_mod_sucesso)
        df_resultado.at[index, col_std_sucesso] = std_mod_sucesso
        df_resultado.at[index, col_min_sucesso] = min_mod_sucesso
        df_resultado.at[index, col_max_sucesso] = max_mod_sucesso

    # Preencher NaN com 0 para evitar problemas na divisão
    df_resultado = df_resultado.fillna(0)

    df_resultado.to_csv(f'{pasta_dados}/{arquivo}_{ano}.csv', index=False, sep=';', decimal=',', encoding='utf-8-sig')

    caminho_arquivo_excel = f'{pasta_dados}/{arquivo}_{ano}.xlsx'
    comum._gravar_excel_formatado(df_resultado, caminho_arquivo_excel, {
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
            df_formatado[coluna] = df_formatado[coluna].map(comum.formatar_int)
        elif coluna =='particip':
            df_formatado[coluna] = df_formatado[coluna].map(comum.formatar_percent)
        elif coluna =='taxa_sucesso':
            df_formatado[coluna] = df_formatado[coluna].map(comum.formatar_percent)
        elif df_formatado[coluna].dtype.name == 'float64':
            df_formatado[coluna] = df_formatado[coluna].map(comum.formatar_numero)

    
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

    mk_table = comum.formatar_com_milhares(df_formatado.to_markdown(index=False, disable_numparse=True, colalign=alinhamento_md))

    with open(f'{pasta_md}/{arquivo}.md', 'w', encoding='utf8') as md_descritivo:
        md_descritivo.write(f'{template.replace("$(nome_dimensao)", titulo)}')

        md_descritivo.write('\n')
        md_descritivo.write(f'{mk_table}')
        md_descritivo.write('\n')

        md_descritivo.close()

    analise_md.append({arquivo: mk_table})

    return True

# gerar o resumo de campanhas por origem e modalidades
def gerar_resumo_por_origem_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    return _gerar_resumo_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, 'origem', analise_md)

# gerar o resumo de campanhas por uf_br
def gerar_resumo_por_ufbr(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    return _gerar_resumo_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, 'geral_uf_br', analise_md)

# gerar o resumo de campanhas por gênero
def gerar_resumo_por_genero(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    return _gerar_resumo_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, 'autoria_classificacao', analise_md)

# gerar o resumo de campanhas por autoria e seus respectivos status
def gerar_resumo_por_autoria(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    return _gerar_resumo_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, 'autoria_nome_publico', analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_resumo_por_mencoes_angelo_agostini(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  'mencoes_angelo_agostini'
    return _gerar_resumo_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_resumo_por_mencoes_ccxp(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  'mencoes_ccxp'
    return _gerar_resumo_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_resumo_por_mencoes_disputa(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  'mencoes_disputa'
    return _gerar_resumo_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_resumo_por_mencoes_erotismo(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  'mencoes_erotismo'
    return _gerar_resumo_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_resumo_por_mencoes_fantasia(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  'mencoes_fantasia'
    return _gerar_resumo_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_resumo_por_mencoes_ficcao_cientifica(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  'mencoes_ficcao_cientifica'
    return _gerar_resumo_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_resumo_por_mencoes_fiq(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  'mencoes_fiq'
    return _gerar_resumo_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_resumo_por_mencoes_folclore(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  'mencoes_folclore'
    return _gerar_resumo_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_resumo_por_mencoes_herois(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  'mencoes_herois'
    return _gerar_resumo_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_resumo_por_mencoes_hqmix(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  'mencoes_hqmix'
    return _gerar_resumo_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_resumo_por_mencoes_humor(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  'mencoes_humor'
    return _gerar_resumo_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_resumo_por_mencoes_jogos(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  'mencoes_jogos'
    return _gerar_resumo_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_resumo_por_mencoes_lgbtqiamais(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  'mencoes_lgbtqiamais'
    return _gerar_resumo_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_resumo_por_mencoes_midia_independente(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  'mencoes_midia_independente'
    return _gerar_resumo_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_resumo_por_mencoes_politica(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  'mencoes_politica'
    return _gerar_resumo_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_resumo_por_mencoes_questoes_genero(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  'mencoes_questoes_genero'
    return _gerar_resumo_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_resumo_por_mencoes_religiosidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  'mencoes_religiosidade'
    return _gerar_resumo_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_resumo_por_mencoes_saloes_humor(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  'mencoes_saloes_humor'
    return _gerar_resumo_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_resumo_por_mencoes_terror(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  'mencoes_terror'
    return _gerar_resumo_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_resumo_por_mencoes_webformatos(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  'mencoes_webformatos'
    return _gerar_resumo_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_resumo_por_mencoes_zine(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  'mencoes_zine'
    return _gerar_resumo_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)
