import pandas as pd

# divide dois números, mas se o divisor for zero, apenas retorna zero
def dividir(dividendo, divisor):
    if divisor == 0:
        return 0
    return dividendo / divisor

# gravar excel formatado
def gravar_excel_formatado(df_resultado, caminho_arquivo_excel, colunas_formato):
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
            col_idx = df_resultado.columns.get_loc(coluna)
            planilha.set_column(col_idx, col_idx, cell_format=writer.book.add_format(formato_excel))

# calcular a quantidade de campanhas por modalidades e seus respectivos status
def calcular_qtd_por_modalidade(df, ano, pasta, arquivo):
    colunas = ['geral_modalidade', 'geral_status']
    df_resultado = df.groupby(colunas).size().reset_index(name='total')

    colunas.append('total')

    #print(df_resultado)

    df_resultado.to_csv(f'{pasta}/{arquivo}_{ano}.csv', index=False, columns=colunas, sep=';', decimal=',', encoding='utf-8-sig')
    caminho_arquivo_excel = f'{pasta}/{arquivo}_{ano}.xlsx'
    gravar_excel_formatado(df_resultado, caminho_arquivo_excel, {
        #'taxa_sucesso': {'num_format': '0.00%'}
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
        col_valor_arrecadado = f'valor_arrecadado'
        col_total_sucesso = f'total_sucesso'
        col_valor_arrecadado_sucesso = f'valor_arrecadado_sucesso'

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
        df_resultado.at[index, col_taxa_sucesso] = dividir(total_mod_sucesso, total_mod)

    # Preencher NaN com 0 para evitar problemas na divisão
    df_resultado = df_resultado.fillna(0)

    #print(df_resultado)
    df_resultado.to_csv(f'{pasta}/{arquivo}_{ano}.csv', index=False, sep=';', decimal=',', encoding='utf-8-sig')

    caminho_arquivo_excel = f'{pasta}/{arquivo}_{ano}.xlsx'
    gravar_excel_formatado(df_resultado, caminho_arquivo_excel, {
        'taxa_sucesso': {'num_format': '0.00%'},
        'valor_arrecadado': {'num_format': 'R$ #,##0.00'},
        'valor_arrecadado_sucesso': {'num_format': 'R$ #,##0.00'},
        })

    return True

# calcular a quantidade de campanhas por origem, modalidades e seus respectivos status
def calcular_qtd_por_origem_modalidade(df, ano, pasta, arquivo):
    colunas = ['origem', 'geral_modalidade', 'geral_status']
    df_resultado = df.groupby(colunas).size().reset_index(name='total')

    colunas.append('total')

    #print(contagem_ocorrencias)

    df_resultado.to_csv(f'{pasta}/{arquivo}_{ano}.csv', index=False, columns=colunas, sep=';', decimal=',', encoding='utf-8-sig')

    caminho_arquivo_excel = f'{pasta}/{arquivo}_{ano}.xlsx'
    gravar_excel_formatado(df_resultado, caminho_arquivo_excel, {
        #'taxa_sucesso': {'num_format': '0.00%'}
        })

    return True

# calcular o resumo de campanhas por origem e modalidades
def calcular_resumo_por_origem_modalidade(df, ano, pasta, arquivo):
    colunas = ['origem', 'geral_modalidade']
    df_resultado = df.groupby(colunas).size().reset_index(name='total')

    # estender o df com mais colunas
    for index, row in df_resultado.iterrows():
        origem = row['origem']
        modalidade = row['geral_modalidade']
        total_origem_mod = row['total']
        col_valor_mod = f'valor_arrecadado'
        col_total_sucesso = f'total_sucesso'
        col_valor_mod_sucesso = f'valor_arrecadado_sucesso'
        col_taxa_sucesso = f'taxa_sucesso'
        col_particip = f'particip'

        campanhas_mod = df[
            (df['geral_modalidade'] == modalidade)
            ]
        total_mod = len(campanhas_mod)
        valor_mod = df[
            (df['origem'] == origem)
            & (df['geral_modalidade'] == modalidade)
            ]['geral_arrecadado_corrigido'].sum()

        if modalidade == 'sub':
            campanhas_origem_mod_sucesso = df[
                (df['origem'] == origem)
                & (df['geral_modalidade'] == modalidade)
                & (df['geral_total_contribuicoes'] > 0)
                ]
            total_origem_mod_sucesso = len(campanhas_origem_mod_sucesso)
            valor_origem_mod_sucesso = campanhas_origem_mod_sucesso['geral_arrecadado_corrigido'].sum()
        else:
            campanhas_origem_mod_sucesso = df[
                (df['origem'] == origem)
                & (df['geral_modalidade'] == modalidade)
                & (df['geral_status'] != 'failed')
                ]
            total_origem_mod_sucesso = len(campanhas_origem_mod_sucesso)
            valor_origem_mod_sucesso = campanhas_origem_mod_sucesso['geral_arrecadado_corrigido'].sum()


        df_resultado.at[index, col_valor_mod] = valor_mod
        df_resultado.at[index, col_total_sucesso] = total_origem_mod_sucesso
        df_resultado.at[index, col_valor_mod_sucesso] = valor_origem_mod_sucesso
        df_resultado.at[index, col_taxa_sucesso] = dividir(total_origem_mod_sucesso, total_mod)
        df_resultado.at[index, col_particip] = dividir(total_origem_mod, total_mod)

    # Preencher NaN com 0 para evitar problemas na divisão
    df_resultado = df_resultado.fillna(0)

    colunas.append('total')

    #print(contagem_ocorrencias)

    df_resultado.to_csv(f'{pasta}/{arquivo}_{ano}.csv', index=False, columns=colunas, sep=';', decimal=',', encoding='utf-8-sig')

    caminho_arquivo_excel = f'{pasta}/{arquivo}_{ano}.xlsx'
    gravar_excel_formatado(df_resultado, caminho_arquivo_excel, {
        'taxa_sucesso': {'num_format': '0.00%'},
        'particip': {'num_format': '0.00%'},
        'valor_arrecadado': {'num_format': 'R$ #,##0.00'},
        'valor_arrecadado_sucesso': {'num_format': 'R$ #,##0.00'},
        })

    return True

# calcular a quantidade de campanhas por uf_br e seus respectivos status
def calcular_qtd_por_ufbr(df, ano, pasta, arquivo):
    colunas = ['geral_uf_br']
    df_resultado = df.groupby(colunas).size().reset_index(name='total')

    # estender o df com mais colunas
    for index, row in df_resultado.iterrows():
        ufbr = row['geral_uf_br']
        total = row['total']

        for modalidade in ['aon', 'flex', 'sub']:
            col_mod = f'{modalidade}'
            col_mod_sucesso = f'{modalidade}_sucesso'
            col_mod_falha = f'{modalidade}_falha'

            # 'total' na modalidade
            campanhas_modalidade = df[
                (df['geral_modalidade'] == modalidade)
                & (df['geral_uf_br'] == ufbr)
                ]
            total_mod = len(campanhas_modalidade)

            if modalidade == 'sub':
                # 'total' na modalidade
                campanhas_modalidade_sucesso = df[
                    (df['geral_modalidade'] == modalidade)
                    & (df['geral_uf_br'] == ufbr)
                    & (df['geral_total_contribuicoes'] > 0)
                    ]
                total_mod_sucesso = len(campanhas_modalidade_sucesso)
            else:
                # 'total' na modalidade
                campanhas_modalidade_sucesso = df[
                    (df['geral_modalidade'] == modalidade)
                    & (df['geral_uf_br'] == ufbr)
                    & (df['geral_status'] != 'failed')
                    ]
                total_mod_sucesso = len(campanhas_modalidade_sucesso)

            total_mod_falha = total_mod - total_mod_sucesso
            df_resultado.at[index, col_mod] = total_mod
            df_resultado.at[index, col_mod_sucesso] = total_mod_sucesso
            df_resultado.at[index, col_mod_falha] = total_mod_falha

    #print(contagem_ocorrencias)

    df_resultado.to_csv(f'{pasta}/{arquivo}_{ano}.csv', index=False, sep=';', decimal=',', encoding='utf-8-sig')

    caminho_arquivo_excel = f'{pasta}/{arquivo}_{ano}.xlsx'
    gravar_excel_formatado(df_resultado, caminho_arquivo_excel, {
        #'taxa_sucesso': {'num_format': '0.00%'}
        })

    return True

# calcular a taxa de sucesso de campanhas por uf_br
def calcular_txsucesso_por_ufbr(df, ano, pasta, arquivo):
    colunas = ['geral_uf_br']
    df_resultado = df.groupby(colunas).size().reset_index(name='total')

    # estender o df com mais colunas
    for index, row in df_resultado.iterrows():
        ufbr = row['geral_uf_br']

        for modalidade in ['aon', 'flex', 'sub']:
            col_mod = f'total_{modalidade}'
            col_mod_sucesso = f'taxa_sucesso_{modalidade}'
            col_mod_partic =  f'particip_{modalidade}'

            campanhas = df[
                (df['geral_modalidade'] == modalidade)
                ]
            total = len(campanhas)

            # 'total' na modalidade
            campanhas_modalidade = df[
                (df['geral_modalidade'] == modalidade)
                & (df['geral_uf_br'] == ufbr)
                ]
            total_mod = len(campanhas_modalidade)

            if modalidade == 'sub':
                # 'total' na modalidade
                campanhas_modalidade_sucesso = df[
                    (df['geral_modalidade'] == modalidade)
                    & (df['geral_uf_br'] == ufbr)
                    & (df['geral_total_contribuicoes'] > 0)
                    ]
                total_mod_sucesso = len(campanhas_modalidade_sucesso)
            else:
                # 'total' na modalidade
                campanhas_modalidade_sucesso = df[
                    (df['geral_modalidade'] == modalidade)
                    & (df['geral_uf_br'] == ufbr)
                    & (df['geral_status'] != 'failed')
                    ]
                total_mod_sucesso = len(campanhas_modalidade_sucesso)

            #total_mod_falha = total_mod - total_mod_sucesso
            df_resultado.at[index, col_mod] = total_mod
            df_resultado.at[index, col_mod_sucesso] = dividir(total_mod_sucesso, total_mod)
            df_resultado.at[index, col_mod_partic] = dividir(total_mod, total)

    #print(contagem_ocorrencias)

    df_resultado.to_csv(f'{pasta}/{arquivo}_{ano}.csv', index=False, sep=';', decimal=',', encoding='utf-8-sig')

    caminho_arquivo_excel = f'{pasta}/{arquivo}_{ano}.xlsx'
    gravar_excel_formatado(df_resultado, caminho_arquivo_excel, {
        'taxa_sucesso_aon': {'num_format': '0.00%'},
        'particip_aon': {'num_format': '0.00%'},
        'taxa_sucesso_flex': {'num_format': '0.00%'},
        'particip_flex': {'num_format': '0.00%'},
        'taxa_sucesso_sub': {'num_format': '0.00%'},
        'particip_sub': {'num_format': '0.00%'},
        })

    return True

# calcular a quantidade de campanhas por gênero e seus respectivos status
def calcular_qtd_por_genero(df, ano, pasta, arquivo):
    colunas = ['autoria_classificacao']
    df_resultado = df.groupby(colunas).size().reset_index(name='total')

    # estender o df com mais colunas
    for index, row in df_resultado.iterrows():
        classificacao = row['autoria_classificacao']
        total = row['total']

        for modalidade in ['aon', 'flex', 'sub']:
            col_mod = f'{modalidade}'
            col_mod_sucesso = f'{modalidade}_sucesso'
            col_mod_falha = f'{modalidade}_falha'

            # 'total' na modalidade
            campanhas_modalidade = df[
                (df['geral_modalidade'] == modalidade)
                & (df['autoria_classificacao'] == classificacao)
                ]
            total_mod = len(campanhas_modalidade)

            if modalidade == 'sub':
                # 'total' na modalidade
                campanhas_modalidade_sucesso = df[
                    (df['geral_modalidade'] == modalidade)
                    & (df['autoria_classificacao'] == classificacao)
                    & (df['geral_total_contribuicoes'] > 0)
                    ]
                total_mod_sucesso = len(campanhas_modalidade_sucesso)
            else:
                # 'total' na modalidade
                campanhas_modalidade_sucesso = df[
                    (df['geral_modalidade'] == modalidade)
                    & (df['autoria_classificacao'] == classificacao)
                    & (df['geral_status'] != 'failed')
                    ]
                total_mod_sucesso = len(campanhas_modalidade_sucesso)

            total_mod_falha = total_mod - total_mod_sucesso
            df_resultado.at[index, col_mod] = total_mod
            df_resultado.at[index, col_mod_sucesso] = total_mod_sucesso
            df_resultado.at[index, col_mod_falha] = total_mod_falha

    #print(contagem_ocorrencias)

    df_resultado.to_csv(f'{pasta}/{arquivo}_{ano}.csv', index=False, sep=';', decimal=',', encoding='utf-8-sig')

    caminho_arquivo_excel = f'{pasta}/{arquivo}_{ano}.xlsx'
    gravar_excel_formatado(df_resultado, caminho_arquivo_excel, {
        #'taxa_sucesso': {'num_format': '0.00%'}
        })

    return True

# calcular a taxa de sucesso de campanhas por gênero
def calcular_txsucesso_por_genero(df, ano, pasta, arquivo):
    colunas = ['autoria_classificacao']
    df_resultado = df.groupby(colunas).size().reset_index(name='total')

    # estender o df com mais colunas
    for index, row in df_resultado.iterrows():
        classificacao = row['autoria_classificacao']

        for modalidade in ['aon', 'flex', 'sub']:
            col_mod = f'total_{modalidade}'
            col_mod_sucesso = f'taxa_sucesso_{modalidade}'
            col_mod_partic =  f'particip_{modalidade}'

            campanhas = df[
                (df['geral_modalidade'] == modalidade)
                ]
            total = len(campanhas)

            # 'total' na modalidade
            campanhas_modalidade = df[
                (df['geral_modalidade'] == modalidade)
                & (df['autoria_classificacao'] == classificacao)
                ]
            total_mod = len(campanhas_modalidade)

            if modalidade == 'sub':
                # 'total' na modalidade
                campanhas_modalidade_sucesso = df[
                    (df['geral_modalidade'] == modalidade)
                    & (df['autoria_classificacao'] == classificacao)
                    & (df['geral_total_contribuicoes'] > 0)
                    ]
                total_mod_sucesso = len(campanhas_modalidade_sucesso)
            else:
                # 'total' na modalidade
                campanhas_modalidade_sucesso = df[
                    (df['geral_modalidade'] == modalidade)
                    & (df['autoria_classificacao'] == classificacao)
                    & (df['geral_status'] != 'failed')
                    ]
                total_mod_sucesso = len(campanhas_modalidade_sucesso)

            #total_mod_falha = total_mod - total_mod_sucesso
            df_resultado.at[index, col_mod] = total_mod
            df_resultado.at[index, col_mod_sucesso] = dividir(total_mod_sucesso, total_mod)
            df_resultado.at[index, col_mod_partic] = dividir(total_mod, total)

    #print(contagem_ocorrencias)

    df_resultado.to_csv(f'{pasta}/{arquivo}_{ano}.csv', index=False, sep=';', decimal=',', encoding='utf-8-sig')

    caminho_arquivo_excel = f'{pasta}/{arquivo}_{ano}.xlsx'
    gravar_excel_formatado(df_resultado, caminho_arquivo_excel, {
        'taxa_sucesso_aon': {'num_format': '0.00%'},
        'particip_aon': {'num_format': '0.00%'},
        'taxa_sucesso_flex': {'num_format': '0.00%'},
        'particip_flex': {'num_format': '0.00%'},
        'taxa_sucesso_sub': {'num_format': '0.00%'},
        'particip_sub': {'num_format': '0.00%'},
        })

    return True

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
            col_total = f'{modalidade}_total'
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

    gravar_excel_formatado(df_resultado, caminho_arquivo_excel, {
        #"taxa_sucesso_aon":{'num_format': '0.00%'},
    })

    return True

# calcular a taxa de sucesso de menção de acordo com a modalidade das campanhas
def calcular_txsucesso_por_mencoes(df, ano, pasta, arquivo):
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
            col_total = f'total_{modalidade}'
            col_taxa_sucesso = f'taxa_sucesso_{modalidade}'
            col_particip = f'particip_{modalidade}'

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
            df_resultado.at[index, col_taxa_sucesso] = dividir(total_mod_mencao_sucesso, total_mod_mencao)
            df_resultado.at[index, col_particip] = dividir(total_mod_mencao, total_mod)


    # Preencher NaN com 0 para evitar problemas na divisão
    df_resultado = df_resultado.fillna(0)

    #print(df_resultado)
    df_resultado.to_csv(f'{pasta}/{arquivo}_{ano}.csv', index=False, sep=';', decimal=',', encoding='utf-8-sig')

    # Especifica o caminho do arquivo Excel
    caminho_arquivo_excel = f'{pasta}/{arquivo}_{ano}.xlsx'

    gravar_excel_formatado(df_resultado, caminho_arquivo_excel, {
        "taxa_sucesso_aon":{'num_format': '0.00%'},
        "particip_aon":{'num_format': '0.00%'},
        "taxa_sucesso_flex":{'num_format': '0.00%'},
        "particip_flex":{'num_format': '0.00%'},
        "taxa_sucesso_sub":{'num_format': '0.00%'},
        "particip_sub":{'num_format': '0.00%'},
    })

    return True

# calcular o valor acumulado de campanhas por origem e seus respectivos status
def calcular_vlr_por_origem(df, ano, pasta, arquivo):
    colunas = ['origem']
    df_resultado = df.groupby(colunas).size().reset_index(name='total')

    # estender o df com mais colunas
    for index, row in df_resultado.iterrows():
        origem = row['origem']
        total = row['total']

        for modalidade in ['aon', 'flex', 'sub']:
            col_mod = f'{modalidade}'
            col_mod_sucesso = f'{modalidade}_sucesso'
            col_mod_falha = f'{modalidade}_falha'

            # 'total' na modalidade
            campanhas_modalidade = df[
                (df['geral_modalidade'] == modalidade)
                & (df['origem'] == origem)
                ]
            valor_mod = campanhas_modalidade['geral_arrecadado_corrigido'].sum()

            if modalidade == 'sub':
                # 'total' na modalidade
                campanhas_modalidade_sucesso = df[
                    (df['geral_modalidade'] == modalidade)
                    & (df['origem'] == origem)
                    & (df['geral_total_contribuicoes'] > 0)
                    ]
                valor_mod_sucesso = campanhas_modalidade_sucesso['geral_arrecadado_corrigido'].sum()
            else:
                # 'total' na modalidade
                campanhas_modalidade_sucesso = df[
                    (df['geral_modalidade'] == modalidade)
                    & (df['origem'] == origem)
                    & (df['geral_status'] != 'failed')
                    ]
                valor_mod_sucesso = campanhas_modalidade_sucesso['geral_arrecadado_corrigido'].sum()

            valor_mod_falha = valor_mod - valor_mod_sucesso
            df_resultado.at[index, col_mod] = valor_mod
            df_resultado.at[index, col_mod_sucesso] = valor_mod_sucesso
            df_resultado.at[index, col_mod_falha] = valor_mod_falha

    #print(contagem_ocorrencias)

    df_resultado.to_csv(f'{pasta}/{arquivo}_{ano}.csv', index=False, sep=';', decimal=',', encoding='utf-8-sig')

    caminho_arquivo_excel = f'{pasta}/{arquivo}_{ano}.xlsx'
    # aon	aon_sucesso	aon_falha	flex	flex_sucesso	flex_falha	sub	sub_sucesso	sub_falha

    gravar_excel_formatado(df_resultado, caminho_arquivo_excel, {
        'aon': {'num_format': 'R$ #,##0.00'},
        'aon_sucesso': {'num_format': 'R$ #,##0.00'},
        'aon_falha': {'num_format': 'R$ #,##0.00'},
        'flex': {'num_format': 'R$ #,##0.00'},
        'flex_sucesso': {'num_format': 'R$ #,##0.00'},
        'flex_falha': {'num_format': 'R$ #,##0.00'},
        'sub': {'num_format': 'R$ #,##0.00'},
        'sub_sucesso': {'num_format': 'R$ #,##0.00'},
        'sub_falha': {'num_format': 'R$ #,##0.00'},
        })

    return True

# calcular o valor acumulado de campanhas por autoria e seus respectivos status
def calcular_vlr_por_autoria(df, ano, pasta, arquivo):
    colunas = ['autoria_nome_publico']
    df_resultado = df.groupby(colunas).size().reset_index(name='total')

    # estender o df com mais colunas
    for index, row in df_resultado.iterrows():
        nome_publico = row['autoria_nome_publico']
        total = row['total']

        for modalidade in ['aon', 'flex', 'sub']:
            col_mod = f'{modalidade}'
            col_mod_sucesso = f'{modalidade}_sucesso'
            col_mod_falha = f'{modalidade}_falha'

            # 'total' na modalidade
            campanhas_modalidade = df[
                (df['geral_modalidade'] == modalidade)
                & (df['autoria_nome_publico'] == nome_publico)
                ]
            valor_mod = campanhas_modalidade['geral_arrecadado_corrigido'].sum()

            if modalidade == 'sub':
                # 'total' na modalidade
                campanhas_modalidade_sucesso = df[
                    (df['geral_modalidade'] == modalidade)
                    & (df['autoria_nome_publico'] == nome_publico)
                    & (df['geral_total_contribuicoes'] > 0)
                    ]
                valor_mod_sucesso = campanhas_modalidade_sucesso['geral_arrecadado_corrigido'].sum()
            else:
                # 'total' na modalidade
                campanhas_modalidade_sucesso = df[
                    (df['geral_modalidade'] == modalidade)
                    & (df['autoria_nome_publico'] == nome_publico)
                    & (df['geral_status'] != 'failed')
                    ]
                valor_mod_sucesso = campanhas_modalidade_sucesso['geral_arrecadado_corrigido'].sum()

            valor_mod_falha = valor_mod - valor_mod_sucesso
            df_resultado.at[index, col_mod] = valor_mod
            df_resultado.at[index, col_mod_sucesso] = valor_mod_sucesso
            df_resultado.at[index, col_mod_falha] = valor_mod_falha

    #print(contagem_ocorrencias)

    df_resultado.to_csv(f'{pasta}/{arquivo}_{ano}.csv', index=False, sep=';', decimal=',', encoding='utf-8-sig')

    caminho_arquivo_excel = f'{pasta}/{arquivo}_{ano}.xlsx'
    # aon	aon_sucesso	aon_falha	flex	flex_sucesso	flex_falha	sub	sub_sucesso	sub_falha

    gravar_excel_formatado(df_resultado, caminho_arquivo_excel, {
        'aon': {'num_format': 'R$ #,##0.00'},
        'aon_sucesso': {'num_format': 'R$ #,##0.00'},
        'aon_falha': {'num_format': 'R$ #,##0.00'},
        'flex': {'num_format': 'R$ #,##0.00'},
        'flex_sucesso': {'num_format': 'R$ #,##0.00'},
        'flex_falha': {'num_format': 'R$ #,##0.00'},
        'sub': {'num_format': 'R$ #,##0.00'},
        'sub_sucesso': {'num_format': 'R$ #,##0.00'},
        'sub_falha': {'num_format': 'R$ #,##0.00'},
        })

    return True

# calcular a quantidade de campanhas por autoria e seus respectivos status
def calcular_qtd_por_autoria(df, ano, pasta, arquivo):
    colunas = ['autoria_nome_publico']
    df_resultado = df.groupby(colunas).size().reset_index(name='total')

    # estender o df com mais colunas
    for index, row in df_resultado.iterrows():
        nome_publico = row['autoria_nome_publico']
        total = row['total']

        for modalidade in ['aon', 'flex', 'sub']:
            col_mod = f'{modalidade}'
            col_mod_sucesso = f'{modalidade}_sucesso'
            col_mod_falha = f'{modalidade}_falha'

            # 'total' na modalidade
            campanhas_modalidade = df[
                (df['geral_modalidade'] == modalidade)
                & (df['autoria_nome_publico'] == nome_publico)
                ]
            total_mod = campanhas_modalidade['geral_arrecadado_corrigido'].count()

            if modalidade == 'sub':
                # 'total' na modalidade
                campanhas_modalidade_sucesso = df[
                    (df['geral_modalidade'] == modalidade)
                    & (df['autoria_nome_publico'] == nome_publico)
                    & (df['geral_total_contribuicoes'] > 0)
                    ]
                total_mod_sucesso = campanhas_modalidade_sucesso['geral_arrecadado_corrigido'].count()
            else:
                # 'total' na modalidade
                campanhas_modalidade_sucesso = df[
                    (df['geral_modalidade'] == modalidade)
                    & (df['autoria_nome_publico'] == nome_publico)
                    & (df['geral_status'] != 'failed')
                    ]
                total_mod_sucesso = campanhas_modalidade_sucesso['geral_arrecadado_corrigido'].count()

            total_mod_falha = total_mod - total_mod_sucesso
            df_resultado.at[index, col_mod] = total_mod
            df_resultado.at[index, col_mod_sucesso] = total_mod_sucesso
            df_resultado.at[index, col_mod_falha] = total_mod_falha

    #print(contagem_ocorrencias)

    df_resultado.to_csv(f'{pasta}/{arquivo}_{ano}.csv', index=False, sep=';', decimal=',', encoding='utf-8-sig')

    caminho_arquivo_excel = f'{pasta}/{arquivo}_{ano}.xlsx'
    # aon	aon_sucesso	aon_falha	flex	flex_sucesso	flex_falha	sub	sub_sucesso	sub_falha

    gravar_excel_formatado(df_resultado, caminho_arquivo_excel, {
        #'aon': {'num_format': 'R$ #,##0.00'},
        })

    return True
