import pandas as pd

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

        # Obtém o objeto de formatação do escritor
        #formato_excel = writer.book.add_format({'num_format': '0.00%'})

        # Obtém o objeto de planilha
        planilha = writer.sheets['Sheet1']

        # Aplica o formato percentual às colunas
        for coluna, formato_excel in colunas_formato.items():
            if coluna in df_resultado.columns:
                col_idx = df_resultado.columns.get_loc(coluna)
                planilha.set_column(col_idx, col_idx, cell_format=writer.book.add_format(formato_excel))

# calcular a quantidade de campanhas por dimensão, modalidades e seus respectivos status
def _calcular_qtd_por_dim_modalidade(df, ano, pasta, arquivo, col_dim):
    colunas = [col_dim]
    df_resultado = df.groupby(colunas).size().reset_index(name='total')

    # estender o df com mais colunas
    for index, row in df_resultado.iterrows():
        dim = row[col_dim]
        total_dim = row['total']

        for modalidade in ['aon', 'flex', 'sub']:

            col_total = f'{modalidade}'
            col_total_sucesso = f'{modalidade}_sucesso'
            col_total_falha = f'{modalidade}_falha'

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
            else:
                campanhas_dim_mod_sucesso = df[
                    (df[col_dim] == dim)
                    & (df['geral_modalidade'] == modalidade)
                    & (df['geral_status'] != 'failed')
                    ]
                total_dim_mod_sucesso = len(campanhas_dim_mod_sucesso)


            df_resultado.at[index, col_total] = total_dim_mod
            df_resultado.at[index, col_total_sucesso] = total_dim_mod_sucesso
            df_resultado.at[index, col_total_falha] = total_dim_mod - total_dim_mod_sucesso

    # Preencher NaN com 0 para evitar problemas na divisão
    df_resultado = df_resultado.fillna(0)

    colunas.append('total')

    #print(contagem_ocorrencias)

    df_resultado.to_csv(f'{pasta}/{arquivo}_{ano}.csv', index=False, columns=colunas, sep=';', decimal=',', encoding='utf-8-sig')

    caminho_arquivo_excel = f'{pasta}/{arquivo}_{ano}.xlsx'
    formatados = {}
    for modalidade in ['aon', 'flex', 'sub']:
        formatados[f'{modalidade}_particip'] = {'num_format': '0.00%'}
        formatados[f'{modalidade}_taxa_sucesso'] = {'num_format': '0.00%'}
        formatados[f'{modalidade}_valor_sucesso'] = {'num_format': 'R$ #,##0.00'}

    _gravar_excel_formatado(df_resultado, caminho_arquivo_excel, formatados)

    return True

# calcular o resumo de campanhas por dim e modalidades
def _calcular_resumo_por_dim_modalidade(df, ano, pasta, arquivo, col_dim):
    colunas = [col_dim]
    df_resultado = df.groupby(colunas).size().reset_index(name='total')

    # estender o df com mais colunas
    for index, row in df_resultado.iterrows():
        dim = row[col_dim]
        total_dim = row['total']

        for modalidade in ['aon', 'flex', 'sub']:

            col_total = f'{modalidade}'
            col_total_sucesso = f'{modalidade}_sucesso'
            col_total_falha = f'{modalidade}_falha'

            col_particip = f'{modalidade}_particip'

            col_taxa_sucesso = f'{modalidade}_taxa_sucesso'
            col_valor_mod_sucesso = f'{modalidade}_valor_sucesso'

            col_media_sucesso = f'{modalidade}_media_sucesso'

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
            else:
                campanhas_dim_mod_sucesso = df[
                    (df[col_dim] == dim)
                    & (df['geral_modalidade'] == modalidade)
                    & (df['geral_status'] != 'failed')
                    ]
                total_dim_mod_sucesso = len(campanhas_dim_mod_sucesso)
                valor_dim_mod_sucesso = campanhas_dim_mod_sucesso['geral_arrecadado_corrigido'].sum()


            df_resultado.at[index, col_total] = total_dim_mod
            df_resultado.at[index, col_total_sucesso] = total_dim_mod_sucesso
            df_resultado.at[index, col_total_falha] = total_dim_mod - total_dim_mod_sucesso

            df_resultado.at[index, col_particip] = _dividir(total_dim_mod, total_mod)

            df_resultado.at[index, col_taxa_sucesso] = _dividir(total_dim_mod_sucesso, total_dim_mod)

            df_resultado.at[index, col_valor_mod_sucesso] = valor_dim_mod_sucesso
            df_resultado.at[index, col_media_sucesso] = _dividir(valor_dim_mod_sucesso, total_dim_mod_sucesso)

    # Preencher NaN com 0 para evitar problemas na divisão
    df_resultado = df_resultado.fillna(0)

    colunas.append('total')

    #print(contagem_ocorrencias)

    df_resultado.to_csv(f'{pasta}/{arquivo}_{ano}.csv', index=False, columns=colunas, sep=';', decimal=',', encoding='utf-8-sig')

    caminho_arquivo_excel = f'{pasta}/{arquivo}_{ano}.xlsx'
    formatados = {}
    for modalidade in ['aon', 'flex', 'sub']:
        formatados[f'{modalidade}_particip'] = {'num_format': '0.00%'}
        formatados[f'{modalidade}_taxa_sucesso'] = {'num_format': '0.00%'}
        formatados[f'{modalidade}_valor_sucesso'] = {'num_format': 'R$ #,##0.00'}
        formatados[f'{modalidade}_media_sucesso'] = {'num_format': 'R$ #,##0.00'}

    _gravar_excel_formatado(df_resultado, caminho_arquivo_excel, formatados)

    return True

# calcular a quantidade de campanhas por modalidades e seus respectivos status
def calcular_qtd_por_modalidade(df, ano, pasta, arquivo):
    colunas = ['geral_modalidade']
    df_resultado = df.groupby(colunas).size().reset_index(name='total')

    # estender o df com mais colunas
    for index, row in df_resultado.iterrows():
        modalidade = row['geral_modalidade']
        total_mod = row['total']

        col_total_sucesso = f'total_sucesso'
        col_total_falha = f'total_falha'

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
        else:
            # 'total_mod_mencao' na modalidade com referência à 'menção' com status diferente de falha
            campanhas_mod_sucesso = df[
                (df['geral_modalidade'] == modalidade)
                & (df['geral_status'] != 'failed')
                ]
            total_mod_sucesso = len(campanhas_mod_sucesso)
        
        df_resultado.at[index, col_total_sucesso] = total_mod_sucesso
        df_resultado.at[index, col_total_falha] = total_mod - total_mod_sucesso

    # Preencher NaN com 0 para evitar problemas na divisão
    df_resultado = df_resultado.fillna(0)

    #print(df_resultado)
    df_resultado.to_csv(f'{pasta}/{arquivo}_{ano}.csv', index=False, sep=';', decimal=',', encoding='utf-8-sig')

    caminho_arquivo_excel = f'{pasta}/{arquivo}_{ano}.xlsx'
    _gravar_excel_formatado(df_resultado, caminho_arquivo_excel, {
        #'taxa_sucesso': {'num_format': '0.00%'},
        #'arrecadado': {'num_format': 'R$ #,##0.00'},
        })

    return True

# calcular a taxa de sucesso de campanhas por modalidades
def calcular_resumo_por_modalidade(df, ano, pasta, arquivo):
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
        else:
            # 'total_mod_mencao' na modalidade com referência à 'menção' com status diferente de falha
            campanhas_mod_sucesso = df[
                (df['geral_modalidade'] == modalidade)
                & (df['geral_status'] != 'failed')
                ]
            total_mod_sucesso = len(campanhas_mod_sucesso)
            valor_mod_sucesso = campanhas_mod_sucesso['geral_arrecadado_corrigido'].sum()
        
        df_resultado.at[index, col_valor_arrecadado] = valor_mod
        df_resultado.at[index, col_total_sucesso] = total_mod_sucesso
        df_resultado.at[index, col_valor_arrecadado_sucesso] = valor_mod_sucesso
        df_resultado.at[index, col_taxa_sucesso] = _dividir(total_mod_sucesso, total_mod)
        df_resultado.at[index, col_media_sucesso] = _dividir(valor_mod_sucesso, total_mod_sucesso)

    # Preencher NaN com 0 para evitar problemas na divisão
    df_resultado = df_resultado.fillna(0)

    #print(df_resultado)
    df_resultado.to_csv(f'{pasta}/{arquivo}_{ano}.csv', index=False, sep=';', decimal=',', encoding='utf-8-sig')

    caminho_arquivo_excel = f'{pasta}/{arquivo}_{ano}.xlsx'
    _gravar_excel_formatado(df_resultado, caminho_arquivo_excel, {
        'taxa_sucesso': {'num_format': '0.00%'},
        'arrecadado': {'num_format': 'R$ #,##0.00'},
        'arrecadado_sucesso': {'num_format': 'R$ #,##0.00'},
        'media_sucesso': {'num_format': 'R$ #,##0.00'},
        })

    return True

# calcular a quantidade de campanhas por origem, modalidades e seus respectivos status
def calcular_qtd_por_origem_modalidade(df, ano, pasta, arquivo):
    return _calcular_qtd_por_dim_modalidade(df, ano, pasta, arquivo, 'origem')

# calcular o resumo de campanhas por origem e modalidades
def calcular_resumo_por_origem_modalidade(df, ano, pasta, arquivo):
    return _calcular_resumo_por_dim_modalidade(df, ano, pasta, arquivo, 'origem')

# calcular a quantidade de campanhas por uf_br e seus respectivos status
def calcular_qtd_por_ufbr(df, ano, pasta, arquivo):
    return _calcular_qtd_por_dim_modalidade(df, ano, pasta, arquivo, 'geral_uf_br')

# calcular o resumo de campanhas por uf_br
def calcular_resumo_por_ufbr(df, ano, pasta, arquivo):
    return _calcular_resumo_por_dim_modalidade(df, ano, pasta, arquivo, 'geral_uf_br')

# calcular a quantidade de campanhas por gênero e seus respectivos status
def calcular_qtd_por_genero(df, ano, pasta, arquivo):
    return _calcular_qtd_por_dim_modalidade(df, ano, pasta, arquivo, 'autoria_classificacao')

# calcular o resumo de campanhas por gênero
def calcular_resumo_por_genero(df, ano, pasta, arquivo):
    return _calcular_resumo_por_dim_modalidade(df, ano, pasta, arquivo, 'autoria_classificacao')

# calcular a quantidade de campanhas por autoria e seus respectivos status
def calcular_qtd_por_autoria(df, ano, pasta, arquivo):
    return _calcular_qtd_por_dim_modalidade(df, ano, pasta, arquivo, 'autoria_nome_publico')

# calcular o resumo de campanhas por autoria e seus respectivos status
def calcular_resumo_por_autoria(df, ano, pasta, arquivo):
    return _calcular_resumo_por_dim_modalidade(df, ano, pasta, arquivo, 'autoria_nome_publico')

# calcular a taxa de sucesso de menção de acordo com a modalidade das campanhas
def calcular_qtd_por_mencoes(df, ano, pasta, arquivo):
    # Criar colunas 'mencão' e 'total'
    df_resultado = pd.DataFrame({
        'menção': df.columns[df.columns.str.startswith('mencoes_')],
        'total': df.filter(like='mencoes_').sum()
    })

    # estender o df com mais colunas
    for index, row in df_resultado.iterrows():
        mencao = row['menção']

        # Criar colunas 'total' e 'taxa_sucesso' para cada modalidade
        for modalidade in ['aon', 'flex', 'sub']:
            col_total = f'{modalidade}'
            col_sucesso = f'{modalidade}_sucesso'
            col_falha = f'{modalidade}_falha'

            # 'total' na modalidade
            campanhas_modalidade = df[
                (df['geral_modalidade'] == modalidade)
                ]
            total_mod = len(campanhas_modalidade)

            # 'total' na modalidade com referência à 'menção'
            campanhas_mod_mencao = df[
                (df['geral_modalidade'] == modalidade)
                & (df[mencao] == True)
                ]
            total_mod_mencao = len(campanhas_mod_mencao)

            if modalidade == 'sub':
                # 'total_mod_mencao' na modalidade com referência à 'menção' com status diferente de falha
                campanhas_mod_mencao_sucesso = df[
                    (df['geral_modalidade'] == modalidade)
                    & (df[mencao] == True)
                    & (df['geral_total_contribuicoes'] > 0)
                    ]
                total_mod_mencao_sucesso = len(campanhas_mod_mencao_sucesso)
            else:
                # 'total_mod_mencao' na modalidade com referência à 'menção' com status diferente de falha
                campanhas_mod_mencao_sucesso = df[
                    (df['geral_modalidade'] == modalidade)
                    & (df[mencao] == True)
                    & (df['geral_status'] != 'failed')
                    ]
                total_mod_mencao_sucesso = len(campanhas_mod_mencao_sucesso)
            
            df_resultado.at[index, 'menção'] = mencao.replace('mencoes_', '')
            df_resultado.at[index, col_total] = total_mod_mencao
            df_resultado.at[index, col_sucesso] = total_mod_mencao_sucesso
            df_resultado.at[index, col_falha] = total_mod_mencao - total_mod_mencao_sucesso


    # Preencher NaN com 0 para evitar problemas na divisão
    df_resultado = df_resultado.fillna(0)

    #print(df_resultado)
    df_resultado.to_csv(f'{pasta}/{arquivo}_{ano}.csv', index=False, sep=';', decimal=',', encoding='utf-8-sig')

    # Especifica o caminho do arquivo Excel
    caminho_arquivo_excel = f'{pasta}/{arquivo}_{ano}.xlsx'

    _gravar_excel_formatado(df_resultado, caminho_arquivo_excel, {
        #"taxa_sucesso_aon":{'num_format': '0.00%'},
    })

    return True

# calcular o resumo de menção de acordo com a modalidade das campanhas
def calcular_resumo_por_mencoes(df, ano, pasta, arquivo):
    # Criar colunas 'mencão' e 'total'
    df_resultado = pd.DataFrame({
        'menção': df.columns[df.columns.str.startswith('mencoes_')],
        'total': df.filter(like='mencoes_').sum()
    })

    # estender o df com mais colunas
    for index, row in df_resultado.iterrows():
        mencao = row['menção']

        # Criar colunas 'total' e 'taxa_sucesso' para cada modalidade
        for modalidade in ['aon', 'flex', 'sub']:
            col_total = f'{modalidade}'
            col_total_sucesso = f'{modalidade}_sucesso'
            col_total_falha = f'{modalidade}_falha'
            col_taxa_sucesso = f'{modalidade}_taxa_sucesso'
            col_particip = f'{modalidade}_particip'
            col_valor_sucesso = f'{modalidade}_valor_sucesso'
            col_media_sucesso = f'{modalidade}_media_sucesso'

            # 'total' na modalidade
            campanhas_modalidade = df[
                (df['geral_modalidade'] == modalidade)
                ]
            total_mod = len(campanhas_modalidade)

            # 'total' na modalidade com referência à 'menção'
            campanhas_mod_mencao = df[
                (df['geral_modalidade'] == modalidade)
                & (df[mencao] == True)
                ]
            total_mod_mencao = len(campanhas_mod_mencao)

            if modalidade == 'sub':
                # 'total_mod_mencao' na modalidade com referência à 'menção' com status diferente de falha
                campanhas_mod_mencao_sucesso = df[
                    (df['geral_modalidade'] == modalidade)
                    & (df[mencao] == True)
                    & (df['geral_total_contribuicoes'] > 0)
                    ]
                total_mod_mencao_sucesso = len(campanhas_mod_mencao_sucesso)
                valor_mod_mencao_sucesso = campanhas_mod_mencao_sucesso['geral_arrecadado_corrigido'].sum()
            else:
                # 'total_mod_mencao' na modalidade com referência à 'menção' com status diferente de falha
                campanhas_mod_mencao_sucesso = df[
                    (df['geral_modalidade'] == modalidade)
                    & (df[mencao] == True)
                    & (df['geral_status'] != 'failed')
                    ]
                total_mod_mencao_sucesso = len(campanhas_mod_mencao_sucesso)
                valor_mod_mencao_sucesso = campanhas_mod_mencao_sucesso['geral_arrecadado_corrigido'].sum()
            
            df_resultado.at[index, 'menção'] = mencao.replace('mencoes_', '')
            df_resultado.at[index, col_total] = total_mod_mencao
            df_resultado.at[index, col_total_sucesso] = total_mod_mencao_sucesso
            df_resultado.at[index, col_total_falha] = total_mod_mencao - total_mod_mencao_sucesso

            df_resultado.at[index, col_particip] = _dividir(total_mod_mencao, total_mod)

            df_resultado.at[index, col_taxa_sucesso] = _dividir(total_mod_mencao_sucesso, total_mod_mencao)

            df_resultado.at[index, col_valor_sucesso] = valor_mod_mencao_sucesso
            
            df_resultado.at[index, col_media_sucesso] = _dividir(valor_mod_mencao_sucesso, total_mod_mencao_sucesso)


    # Preencher NaN com 0 para evitar problemas na divisão
    df_resultado = df_resultado.fillna(0)

    #print(df_resultado)
    df_resultado.to_csv(f'{pasta}/{arquivo}_{ano}.csv', index=False, sep=';', decimal=',', encoding='utf-8-sig')

    # Especifica o caminho do arquivo Excel
    caminho_arquivo_excel = f'{pasta}/{arquivo}_{ano}.xlsx'
    formatados = {}
    for modalidade in ['aon', 'flex', 'sub']:
        formatados[f'{modalidade}_particip'] = {'num_format': '0.00%'}
        formatados[f'{modalidade}_taxa_sucesso'] = {'num_format': '0.00%'}
        formatados[f'{modalidade}_valor_sucesso'] = {'num_format': 'R$ #,##0.00'}
        formatados[f'{modalidade}_media_sucesso'] = {'num_format': 'R$ #,##0.00'}

    _gravar_excel_formatado(df_resultado, caminho_arquivo_excel,formatados)

    return True
