import colunas as colunaslib
import pandas as pd
import analises.analises_comum as comum

import matplotlib.pyplot as plt
import networkx as nx

# gerar o resumo de campanhas por dim e modalidades
def _gerar_resumo_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col_dim, analise_md):

    df_resultado = comum._calcular_resumo_por_dim_modalidade(df, col_dim)

    colunas = df_resultado.columns

    df_resultado.to_csv(f'{pasta_dados}/{arquivo}_{ano}.csv', index=False, columns=colunas, sep=';', decimal=',', encoding='utf-8-sig')

    caminho_arquivo_excel = f'{pasta_dados}/{arquivo}_{ano}.xlsx'
    formatados = {}
    formatados[f'particip'] = {'num_format': '0.00%'}
    formatados[f'taxa_sucesso'] = {'num_format': '0.00%'}
    formatados[f'arrecadado_sucesso'] = {'num_format': 'R$ #,##0.00'}
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

    mermaid = ''
    if (arquivo=='sint_resumo_por_origem_modalidade'):
        for orig in ['catarse', 'apoia.se']:
            if orig == 'catarse':
                origens = ['Catarse']
            else:
                origens = ['Apoia.se']

            mermaid = mermaid + _gerar_mermaid(
                df[
                    (df[colunaslib.COL_ORIGEM]==orig)
                ], df_resultado[
                    (df_resultado[colunaslib.COL_ORIGEM]==orig)
                ], origens)



    alinhamento_md = []
    for c in df_resultado.columns:
        d = df_resultado[c].dtype.name
        if d == 'int64':
            alinhamento_md.append('right')
        elif d == 'float64':
            alinhamento_md.append('right')
        else:
            alinhamento_md.append('left')

    df_formatado[colunaslib.COL_GERAL_MODALIDADE] = df_formatado[colunaslib.COL_GERAL_MODALIDADE].map(comum.TITULOS_MODALIDADES_LOWER)
    df_formatado.rename(columns={colunaslib.COL_GERAL_MODALIDADE: 'modalidade'}, inplace=True)

    mk_table = comum.formatar_tabelamarkdown_com_milhares(df_formatado.to_markdown(index=False, disable_numparse=True, colalign=alinhamento_md))

    with open(f'{pasta_md}/{arquivo}.md', 'w', encoding='utf8') as md_descritivo:
        md_descritivo.write(f'{template.replace("$(nome_dimensao)", titulo)}')

        md_descritivo.write('\n')
        md_descritivo.write(f'{mk_table}')
        md_descritivo.write('\n')

        if mermaid != '':
            md_descritivo.write('\n')
            md_descritivo.write(mermaid)
            md_descritivo.write('\n')

        md_descritivo.close()


    analise_md.append({arquivo: mk_table})

    return True

def _gerar_string_origens(origens):
    if len(origens)==1:
        return origens[0]
    
    buffer = ''
    i = 1
    for it in origens:
        if i > 1:
            if i == len(origens):
                buffer = buffer + ' e '
            else:
                buffer = buffer + ', '
        buffer = buffer + it
        i = i + 1

    return buffer

def _gerar_mermaid(df, df_resumo, origens):

    col_arrecadado_sucesso = 'arrecadado_sucesso'

    mermaid = ''

    total_campanhas = df_resumo['total'].sum()
    menor_ano = df['ano'].min()
    maior_ano = df['ano'].max()

    total_campanhas_pontuais = 0
    total_campanhas_aon = 0
    total_campanhas_flex = 0
    total_campanhas_sub = 0

    taxa_sucesso_aon = 0.0
    taxa_sucesso_flex = 0.0
    taxa_sucesso_sub = 0.0

    arrecadado_sucesso_aon = 0.0
    arrecadado_sucesso_flex = 0.0
    arrecadado_sucesso_sub = 0.0

    media_sucesso_aon = 0.0
    media_sucesso_flex = 0.0
    media_sucesso_sub = 0.0

    for index, row in df_resumo.iterrows():
        modalidade = row[colunaslib.COL_GERAL_MODALIDADE]
        if modalidade == comum.CAMPANHA_AON:
            total_campanhas_aon = row['total']
            total_campanhas_pontuais = total_campanhas_pontuais + total_campanhas_aon
            taxa_sucesso_aon = row['taxa_sucesso']
            arrecadado_sucesso_aon = row[col_arrecadado_sucesso]
            media_sucesso_aon = row['media_sucesso']
        elif modalidade == comum.CAMPANHA_FLEX:
            total_campanhas_flex = row['total']
            total_campanhas_pontuais = total_campanhas_pontuais + total_campanhas_flex
            taxa_sucesso_flex = row['taxa_sucesso']
            arrecadado_sucesso_flex = row[col_arrecadado_sucesso]
            media_sucesso_flex = row['media_sucesso']
        else:
            total_campanhas_sub = row['total']
            taxa_sucesso_sub = row['taxa_sucesso']
            arrecadado_sucesso_sub = row[col_arrecadado_sucesso]
            media_sucesso_sub = row['media_sucesso']


    mermaid = mermaid + f'\n'
    if len(origens)==1:
        mermaid = mermaid + f'## Infográfico - Visão Geral: {_gerar_string_origens(origens)}\n'
    else:
        mermaid = mermaid + f'## Infográfico - Visão Geral\n'
    mermaid = mermaid + f'\n'
    mermaid = mermaid + f'O infográfico a seguir indica um total de {total_campanhas} campanhas em {_gerar_string_origens(origens)},\n'
    mermaid = mermaid + f'entre {menor_ano} e {maior_ano}. As campanhas pontuais totalizam {total_campanhas_pontuais} campanhas, agrupadas\n'
    mermaid = mermaid + f'em {total_campanhas_aon} {comum.TITULOS_MODALIDADES_LOWER[comum.CAMPANHA_AON]} e {total_campanhas_flex} {comum.TITULOS_MODALIDADES_LOWER[comum.CAMPANHA_FLEX]}. As campanhas recorrentes estão em {total_campanhas_sub}.\n'
    mermaid = mermaid + f'A taxa de sucesso, o total arrecadado e a média de arrecadação por campanha\n'
    mermaid = mermaid + f'são apresentados para cada modalidade e compreendem uma visão alternativa\n'
    mermaid = mermaid + f'à tabela apresentada inicialmente.\n'
    mermaid = mermaid + f'\n'

    mermaid = mermaid + f'```mermaid\n'
    mermaid = mermaid + f'mindmap\n'
    mermaid = mermaid + f'  root(("{total_campanhas} campanhas em Catarse e Apoia.se ({menor_ano}-{maior_ano})"))\n'
    mermaid = mermaid + f'    camp_pontual("{total_campanhas_pontuais} campanhas pontuais")\n'
    mermaid = mermaid + f'        camp_pontual_tudo_ou_nada("{total_campanhas_aon} {comum.TITULOS_MODALIDADES_LOWER[comum.CAMPANHA_AON]}")\n'
    mermaid = mermaid + f'            camp_pontual_tudo_ou_nada_taxa_sucesso["{comum.formatar_percent(taxa_sucesso_aon).replace(".", ",")}% taxa de sucesso"]\n'
    mermaid = mermaid + f'            camp_pontual_tudo_ou_nada_arr["R$ {comum.formatar_com_milhares(arrecadado_sucesso_aon)} total arrecadado"]\n'
    mermaid = mermaid + f'            camp_pontual_tudo_ou_nada_arr_med["R$ {comum.formatar_com_milhares(media_sucesso_aon)}/campanha arrecadação média"]\n'
    mermaid = mermaid + f'        camp_pontual_flex("{total_campanhas_flex} {comum.TITULOS_MODALIDADES_LOWER[comum.CAMPANHA_FLEX]}")\n'
    mermaid = mermaid + f'            camp_pontual_flex_taxa_sucesso["{comum.formatar_percent(taxa_sucesso_flex).replace(".", ",")}% taxa de sucesso"]\n'
    mermaid = mermaid + f'            camp_pontual_flex_arr_mensal["R$ {comum.formatar_com_milhares(arrecadado_sucesso_flex)} total arrecadado"]\n'
    mermaid = mermaid + f'            camp_pontual_flex_arr_med_mensal["R$ {comum.formatar_com_milhares(media_sucesso_flex)}/campanha arrecadação média"]\n'
    mermaid = mermaid + f'    camp_recorrente("{total_campanhas_sub} campanhas recorrentes")\n'
    mermaid = mermaid + f'        camp_recorrente_taxa_sucesso["{comum.formatar_percent(taxa_sucesso_sub).replace(".", ",")}% taxa de sucesso"]\n'
    mermaid = mermaid + f'        camp_recorrente_arr_mensal["R$ {comum.formatar_com_milhares(arrecadado_sucesso_sub)} arrecadado mensal"]\n'
    mermaid = mermaid + f'        camp_recorrente_arr_med_mensal["R$ {comum.formatar_com_milhares(media_sucesso_sub)}/campanha arrecadação média mensal"]\n'

    mermaid = mermaid + f'```\n'

    return mermaid

# calcular a taxa de sucesso de campanhas por modalidades
def gerar_resumo_por_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    colunas = [colunaslib.COL_GERAL_MODALIDADE]
    df_resultado = df.groupby(colunas).size().reset_index(name='total')

    # estender o df com mais colunas
    for index, row in df_resultado.iterrows():
        modalidade = row[colunaslib.COL_GERAL_MODALIDADE]
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
            (df[colunaslib.COL_GERAL_MODALIDADE] == modalidade)
            ]
        valor_mod = campanhas_mod[colunaslib.COL_GERAL_ARRECADADO_CORRIGIDO].sum()

        if modalidade == comum.CAMPANHA_SUB:
            # 'total_mod_mencao' na modalidade com referência à 'menção' com status diferente de falha
            campanhas_mod_sucesso = df[
                (df[colunaslib.COL_GERAL_MODALIDADE] == modalidade)
                & (df[colunaslib.COL_GERAL_TOTAL_CONTRIBUICOES] > 0)
                ]
            total_mod_sucesso = len(campanhas_mod_sucesso)
            valor_mod_sucesso = campanhas_mod_sucesso[colunaslib.COL_GERAL_ARRECADADO_CORRIGIDO].sum()
            std_mod_sucesso = campanhas_mod_sucesso[colunaslib.COL_GERAL_ARRECADADO_CORRIGIDO].std()
            min_mod_sucesso = campanhas_mod_sucesso[colunaslib.COL_GERAL_ARRECADADO_CORRIGIDO].min()
            max_mod_sucesso = campanhas_mod_sucesso[colunaslib.COL_GERAL_ARRECADADO_CORRIGIDO].max()
        else:
            # 'total_mod_mencao' na modalidade com referência à 'menção' com status diferente de falha
            campanhas_mod_sucesso = df[
                (df[colunaslib.COL_GERAL_MODALIDADE] == modalidade)
                & (df[colunaslib.COL_GERAL_STATUS] != 'failed')
                ]
            total_mod_sucesso = len(campanhas_mod_sucesso)
            valor_mod_sucesso = campanhas_mod_sucesso[colunaslib.COL_GERAL_ARRECADADO_CORRIGIDO].sum()
            std_mod_sucesso = campanhas_mod_sucesso[colunaslib.COL_GERAL_ARRECADADO_CORRIGIDO].std()
            min_mod_sucesso = campanhas_mod_sucesso[colunaslib.COL_GERAL_ARRECADADO_CORRIGIDO].min()
            max_mod_sucesso = campanhas_mod_sucesso[colunaslib.COL_GERAL_ARRECADADO_CORRIGIDO].max()
        
        df_resultado.at[index, col_valor_arrecadado] = valor_mod
        df_resultado.at[index, col_total_sucesso] = int(total_mod_sucesso)
        df_resultado.at[index, col_valor_arrecadado_sucesso] = valor_mod_sucesso
        df_resultado.at[index, col_taxa_sucesso] = comum._dividir(total_mod_sucesso, total_mod)
        df_resultado.at[index, col_media_sucesso] = comum._dividir(valor_mod_sucesso, total_mod_sucesso)
        df_resultado.at[index, col_std_sucesso] = std_mod_sucesso
        df_resultado.at[index, col_min_sucesso] = min_mod_sucesso
        df_resultado.at[index, col_max_sucesso] = max_mod_sucesso

    mermaid = _gerar_mermaid(df, df_resultado, ['Catarse', 'Apoia.se'])

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

    df_formatado[colunaslib.COL_GERAL_MODALIDADE] = df_formatado[colunaslib.COL_GERAL_MODALIDADE].map(comum.TITULOS_MODALIDADES_LOWER)
    df_formatado.rename(columns={colunaslib.COL_GERAL_MODALIDADE: 'modalidade'}, inplace=True)

    mk_table = comum.formatar_tabelamarkdown_com_milhares(df_formatado.to_markdown(index=False, disable_numparse=True, colalign=alinhamento_md))

    with open(f'{pasta_md}/{arquivo}.md', 'w', encoding='utf8') as md_descritivo:
        md_descritivo.write(f'{template.replace("$(nome_dimensao)", titulo)}')

        md_descritivo.write('\n')
        md_descritivo.write(f'{mk_table}')
        md_descritivo.write('\n')

        md_descritivo.write('\n')
        md_descritivo.write(mermaid)
        md_descritivo.write('\n')


        md_descritivo.close()

    analise_md.append({arquivo: mk_table})




    return True

# gerar o resumo de campanhas por origem e modalidades
def gerar_resumo_por_origem_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    return _gerar_resumo_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, colunaslib.COL_ORIGEM, analise_md)

# gerar o resumo de campanhas por uf_br
def gerar_resumo_por_ufbr(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    return _gerar_resumo_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, colunaslib.COL_GERAL_UF_BR, analise_md)

# gerar o resumo de campanhas por gênero
def gerar_resumo_por_genero(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    return _gerar_resumo_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, colunaslib.COL_AUTORIA_CLASSIFICACAO, analise_md)

# gerar o resumo de campanhas por autoria e seus respectivos status
def gerar_resumo_por_autoria(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    return _gerar_resumo_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, colunaslib.COL_AUTORIA_NOME_PUBLICO, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_resumo_por_mencoes_angelo_agostini(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  colunaslib.COL_MENCOES_ANGELO_AGOSTINI
    return _gerar_resumo_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_resumo_por_mencoes_ccxp(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  colunaslib.COL_MENCOES_CCXP
    return _gerar_resumo_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_resumo_por_mencoes_disputa(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  colunaslib.COL_MENCOES_DISPUTA
    return _gerar_resumo_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_resumo_por_mencoes_erotismo(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  colunaslib.COL_MENCOES_EROTISMO
    return _gerar_resumo_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_resumo_por_mencoes_fantasia(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  colunaslib.COL_MENCOES_FANTASIA
    return _gerar_resumo_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_resumo_por_mencoes_ficcao_cientifica(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  colunaslib.COL_MENCOES_FICCAO_CIENTIFICA
    return _gerar_resumo_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_resumo_por_mencoes_fiq(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  colunaslib.COL_MENCOES_FIQ
    return _gerar_resumo_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_resumo_por_mencoes_folclore(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  colunaslib.COL_MENCOES_FOLCLORE
    return _gerar_resumo_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_resumo_por_mencoes_herois(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  colunaslib.COL_MENCOES_HEROIS
    return _gerar_resumo_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_resumo_por_mencoes_hqmix(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  colunaslib.COL_MENCOES_HQMIX
    return _gerar_resumo_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_resumo_por_mencoes_humor(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  colunaslib.COL_MENCOES_HUMOR
    return _gerar_resumo_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_resumo_por_mencoes_jogos(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  colunaslib.COL_MENCOES_JOGOS
    return _gerar_resumo_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_resumo_por_mencoes_lgbtqiamais(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  colunaslib.COL_MENCOES_LGBTQIAMAIS
    return _gerar_resumo_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_resumo_por_mencoes_midia_independente(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  colunaslib.COL_MENCOES_MIDIA_INDEPENDENTE
    return _gerar_resumo_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_resumo_por_mencoes_politica(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  colunaslib.COL_MENCOES_POLITICA
    return _gerar_resumo_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_resumo_por_mencoes_questoes_genero(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  colunaslib.COL_MENCOES_QUESTOES_GENERO
    return _gerar_resumo_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_resumo_por_mencoes_religiosidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  colunaslib.COL_MENCOES_RELIGIOSIDADE
    return _gerar_resumo_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_resumo_por_mencoes_saloes_humor(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  colunaslib.COL_MENCOES_SALOES_HUMOR
    return _gerar_resumo_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_resumo_por_mencoes_terror(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  colunaslib.COL_MENCOES_TERROR
    return _gerar_resumo_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_resumo_por_mencoes_webformatos(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  colunaslib.COL_MENCOES_WEBFORMATOS
    return _gerar_resumo_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_resumo_por_mencoes_zine(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  colunaslib.COL_MENCOES_ZINE
    return _gerar_resumo_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)
