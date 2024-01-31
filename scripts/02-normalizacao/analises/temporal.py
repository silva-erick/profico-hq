import colunas as colunaslib
import pandas as pd
import analises.analises_comum as comum
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


# gerar o resumo de campanhas por dim e modalidades
def _gerar_serie_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col_dim, analise_md):

    df_resultado = comum._calcular_serie_por_dim_modalidade(df, comum.CAMPANHA_AON, col_dim)

    colunas = df_resultado.columns

    df_resultado.to_csv(f'{pasta_dados}/{arquivo}_{ano}.csv', index=False, columns=colunas, sep=';', decimal=',', encoding='utf-8-sig')

    caminho_arquivo_excel = f'{pasta_dados}/{arquivo}_{ano}.xlsx'
    formatados = {}
    formatados[comum.DFCOL_TAXA_SUCESSO] = {'num_format': '0.00%'}
    formatados[comum.DFCOL_ARRECADADO_SUCESSO] = {'num_format': 'R$ #,##0.00'}
    formatados[comum.DFCOL_MEDIA_SUCESSO] = {'num_format': 'R$ #,##0.00'}

    comum._gravar_excel_formatado(df_resultado, caminho_arquivo_excel, formatados)

    df_formatado = df_resultado.copy()

    for coluna in df_formatado.columns:
        if coluna.startswith(comum.DFCOL_TOTAL):
            df_formatado[coluna] = df_formatado[coluna].map(comum.formatar_int)
        elif coluna ==comum.DFCOL_TAXA_SUCESSO:
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

        md_descritivo.close()


    analise_md.append({arquivo: mk_table})

    return True

# formatar moeda
def numero_moeda(valor, pos):
    return f'R$ {valor:,.0f}'.replace(',', '_').replace('.', ',').replace('_', '.')

# formatar porcento
def numero_porcento(valor, pos):
    valor = valor * 100
    return f'{valor:,.1f}%'.replace(',', '_').replace('.', ',').replace('_', '.')

# formatar inteiro
def numero_inteiro(valor, pos):
    return comum.formatar_int(str(valor))

def _gerar_grafico(df_resultado, col_dim, pasta_md, arquivo, tipo_grafico, titulo, eixo_x, eixo_y, funcao_formatacao):
    plt.figure(figsize=(10, 6))
    plt.plot(df_resultado[comum.DFCOL_ANO], df_resultado[col_dim], marker='o', linestyle='-')

    # Adicionar etiquetas em cada ponto de dado
    for i, (ano, valor) in enumerate(zip(df_resultado[comum.DFCOL_ANO], df_resultado[col_dim])):
        plt.text(ano, valor, funcao_formatacao(valor, 0), ha='left', va='bottom')

    plt.title(titulo)
    plt.xlabel(eixo_x)
    plt.ylabel(eixo_y)

    # Usar números sem notação científica no eixo y
    formatter = FuncFormatter(funcao_formatacao)
    plt.gca().yaxis.set_major_formatter(formatter)

    plt.grid(True)

    # Salvar o gráfico como uma imagem (por exemplo, PNG)
    plt.savefig(f'{pasta_md}/{arquivo}-{tipo_grafico}.png')

    plt.close('all')


# calcular a série anual de campanhas por uma modalidade
def _gerar_serie_por_modalidade(df, ano, modalidade, nome_modalidade, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):

    colunas = [comum.DFCOL_ANO]
    df_resultado = df[
        df[colunaslib.COL_GERAL_MODALIDADE] == modalidade
    ].groupby(colunas).size().reset_index(name=comum.DFCOL_TOTAL)

    # estender o df com mais colunas
    for index, row in df_resultado.iterrows():
        ano_analise = row[comum.DFCOL_ANO]
        total_mod = row[comum.DFCOL_TOTAL]

        if modalidade == comum.CAMPANHA_SUB:
            # 'total_mod_mencao' na modalidade com referência à 'menção' com status diferente de falha
            campanhas_mod_sucesso = df[
                (df[colunaslib.COL_GERAL_MODALIDADE] == modalidade)
                & (df[colunaslib.COL_GERAL_TOTAL_CONTRIBUICOES] > 0)
                & (df[comum.DFCOL_ANO] == ano_analise)
                ]
            total_mod_sucesso = len(campanhas_mod_sucesso)
            valor_mod_sucesso = campanhas_mod_sucesso[colunaslib.COL_GERAL_ARRECADADO_CORRIGIDO].sum()
            std_mod_sucesso = campanhas_mod_sucesso[colunaslib.COL_GERAL_ARRECADADO_CORRIGIDO].std()
            min_mod_sucesso = campanhas_mod_sucesso[colunaslib.COL_GERAL_ARRECADADO_CORRIGIDO].min()
            max_mod_sucesso = campanhas_mod_sucesso[colunaslib.COL_GERAL_ARRECADADO_CORRIGIDO].max()
            contribuicoes = campanhas_mod_sucesso[colunaslib.COL_GERAL_TOTAL_CONTRIBUICOES].sum()
        else:
            # 'total_mod_mencao' na modalidade com referência à 'menção' com status diferente de falha
            campanhas_mod_sucesso = df[
                (df[colunaslib.COL_GERAL_MODALIDADE] == modalidade)
                & (df[colunaslib.COL_GERAL_STATUS] != 'failed')
                & (df[comum.DFCOL_ANO] == ano_analise)
                ]
            total_mod_sucesso = len(campanhas_mod_sucesso)
            valor_mod_sucesso = campanhas_mod_sucesso[colunaslib.COL_GERAL_ARRECADADO_CORRIGIDO].sum()
            std_mod_sucesso = campanhas_mod_sucesso[colunaslib.COL_GERAL_ARRECADADO_CORRIGIDO].std()
            min_mod_sucesso = campanhas_mod_sucesso[colunaslib.COL_GERAL_ARRECADADO_CORRIGIDO].min()
            max_mod_sucesso = campanhas_mod_sucesso[colunaslib.COL_GERAL_ARRECADADO_CORRIGIDO].max()
            contribuicoes = campanhas_mod_sucesso[colunaslib.COL_GERAL_TOTAL_CONTRIBUICOES].sum()
        
        df_resultado.at[index, comum.DFCOL_TOTAL] = int(total_mod)
        df_resultado.at[index, comum.DFCOL_TOTAL_SUCESSO] = int(total_mod_sucesso)
        df_resultado.at[index, comum.DFCOL_PARTICIP] = 100 * comum._dividir(total_mod, total_mod)
        df_resultado.at[index, comum.DFCOL_TAXA_SUCESSO] = 100 * comum._dividir(total_mod_sucesso, total_mod)

        df_resultado.at[index, comum.DFCOL_ARRECADADO_SUCESSO] = valor_mod_sucesso
        df_resultado.at[index, comum.DFCOL_MEDIA_SUCESSO] = comum._dividir(valor_mod_sucesso, total_mod_sucesso)
        df_resultado.at[index, comum.DFCOL_STD_SUCESSO] = std_mod_sucesso
        df_resultado.at[index, comum.DFCOL_MIN_SUCESSO] = min_mod_sucesso
        df_resultado.at[index, comum.DFCOL_MAX_SUCESSO] = max_mod_sucesso

        df_resultado.at[index, comum.DFCOL_APOIO_MEDIO] = comum._dividir(valor_mod_sucesso, contribuicoes)
        df_resultado.at[index, comum.DFCOL_CONTRIBUICOES] = contribuicoes
        df_resultado.at[index, comum.DFCOL_MEDIA_CONTRIBUICOES] = comum._dividir(contribuicoes, total_mod_sucesso)

    # Preencher NaN com 0 para evitar problemas na divisão
    df_resultado = df_resultado.fillna(0)

    df_resultado.to_csv(f'{pasta_dados}/{arquivo}_{ano}.csv', index=False, sep=';', decimal=',', encoding='utf-8-sig')

    caminho_arquivo_excel = f'{pasta_dados}/{arquivo}_{ano}.xlsx'
    comum._gravar_excel_formatado(df_resultado, caminho_arquivo_excel, {
        comum.DFCOL_TAXA_SUCESSO: {'num_format': '0.00%'},
        comum.DFCOL_ARRECADADO_SUCESSO: {'num_format': 'R$ #,##0.00'},
        comum.DFCOL_MEDIA_SUCESSO: {'num_format': 'R$ #,##0.00'},
        })

    if modalidade == comum.CAMPANHA_SUB:
        _gerar_grafico(df_resultado, comum.DFCOL_TOTAL, pasta_md, arquivo, 'campanhas', f'Modalidade {nome_modalidade}: Ano de Início da Campanha', 'Ano', 'Campanhas', numero_inteiro)
        _gerar_grafico(df_resultado, comum.DFCOL_TOTAL_SUCESSO, pasta_md, arquivo, 'bem-sucedidas', f'Modalidade {nome_modalidade}: Total de Campanhas bem Sucedidas/Ano de Início da Campanha', 'Ano', 'Campanhas', numero_inteiro)
        _gerar_grafico(df_resultado, comum.DFCOL_ARRECADADO_SUCESSO, pasta_md, arquivo, 'arrecadado', f'Modalidade {nome_modalidade}: Arrecadação Atual/Ano de Início da Campanha', 'Ano', 'Arrecadação', numero_moeda)
        _gerar_grafico(df_resultado, comum.DFCOL_TAXA_SUCESSO, pasta_md, arquivo, 'taxa-sucesso', f'Modalidade {nome_modalidade}: Taxa de Sucesso Atual/Ano de Início da Campanha', 'Ano', 'Taxa de Sucesso', numero_porcento)
        _gerar_grafico(df_resultado, comum.DFCOL_MEDIA_SUCESSO, pasta_md, arquivo, 'media-sucesso', f'Modalidade {nome_modalidade}: Média Arrecadada Atual/Ano de Início da Campanha', 'Ano', 'Média', numero_moeda)
    else:
        _gerar_grafico(df_resultado, comum.DFCOL_TOTAL, pasta_md, arquivo, 'campanhas', f'Modalidade {nome_modalidade}: Total de Campanhas', 'Ano', 'Campanhas', numero_inteiro)
        _gerar_grafico(df_resultado, comum.DFCOL_TOTAL_SUCESSO, pasta_md, arquivo, 'bem-sucedidas', f'Modalidade {nome_modalidade}: Total de Campanhas bem Sucedidas', 'Ano', 'Campanhas', numero_inteiro)
        _gerar_grafico(df_resultado, comum.DFCOL_ARRECADADO_SUCESSO, pasta_md, arquivo, 'arrecadado', f'Modalidade {nome_modalidade}: Arrecadação Anual', 'Ano', 'Arrecadação', numero_moeda)
        _gerar_grafico(df_resultado, comum.DFCOL_TAXA_SUCESSO, pasta_md, arquivo, 'taxa-sucesso', f'Modalidade {nome_modalidade}: Taxa de Sucesso', 'Ano', 'Taxa de Sucesso', numero_porcento)
        _gerar_grafico(df_resultado, comum.DFCOL_MEDIA_SUCESSO, pasta_md, arquivo, 'media-sucesso', f'Modalidade {nome_modalidade}: Média Arrecadada', 'Ano', 'Média', numero_moeda)

    
    df_formatado = df_resultado.copy()

    for coluna in df_formatado.columns:
        if coluna.startswith(comum.DFCOL_TOTAL):
            df_formatado[coluna] = df_formatado[coluna].map(comum.formatar_int)
        elif coluna == comum.DFCOL_ANO:
            df_formatado[coluna] = df_formatado[coluna].map(comum.formatar_nada)
        elif coluna ==comum.DFCOL_TAXA_SUCESSO:
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

    mk_table = comum.formatar_tabelamarkdown_com_milhares(df_formatado.to_markdown(index=False, disable_numparse=True, colalign=alinhamento_md))

    with open(f'{pasta_md}/{arquivo}.md', 'w', encoding='utf8') as md_descritivo:
        md_descritivo.write(f'{template.replace("$(nome_dimensao)", titulo).replace("$(nome_modalidade)", nome_modalidade)}')

        md_descritivo.write('\n')
        md_descritivo.write(f'{mk_table}')
        md_descritivo.write('\n')
        md_descritivo.write('\n')
        md_descritivo.write(f'## Gráficos')
        md_descritivo.write('\n')
        md_descritivo.write('\n')
        md_descritivo.write(f'Série anual. Modalidade {nome_modalidade}: Total de Campanhas.')
        md_descritivo.write('\n')
        md_descritivo.write('\n')
        md_descritivo.write(f'![Gráfico XY com o título "Modalidade {nome_modalidade}: Total de Campanhas". O eixo X é uma escala de anos. O eixo Y é uma escala valores inteiros.](./{arquivo}-campanhas.png "Modalidade {nome_modalidade}: Total de Campanhas")')
        md_descritivo.write('\n')
        md_descritivo.write('\n')
        md_descritivo.write(f'Série anual. Modalidade {nome_modalidade}: Total de Campanhas bem Sucedidas.')
        md_descritivo.write('\n')
        md_descritivo.write('\n')
        md_descritivo.write(f'![Gráfico XY com o título "Modalidade {nome_modalidade}: Total de Campanhas bem Sucedidas". O eixo X é uma escala de anos. O eixo Y é uma escala valores inteiros.](./{arquivo}-bem-sucedidas.png "Modalidade {nome_modalidade}: Total de Campanhas bem Sucedidas")')
        md_descritivo.write('\n')
        md_descritivo.write('\n')
        md_descritivo.write(f'Série anual. Modalidade {nome_modalidade}: Arrecadação Anual.')
        md_descritivo.write('\n')
        md_descritivo.write('\n')
        md_descritivo.write(f'![Gráfico XY com o título "Modalidade {nome_modalidade}: Arrecadação Anual". O eixo X é uma escala de anos. O eixo Y é uma escala valores monetários.](./{arquivo}-arrecadado.png "Modalidade {nome_modalidade}: Arrecadação Anual")')
        md_descritivo.write('\n')
        md_descritivo.write('\n')
        md_descritivo.write(f'Série anual. Modalidade {nome_modalidade}: Taxa de Sucesso.')
        md_descritivo.write('\n')
        md_descritivo.write('\n')
        md_descritivo.write(f'![Gráfico XY com o título "Modalidade {nome_modalidade}: Taxa de Sucesso". O eixo X é uma escala de anos. O eixo Y é uma escala de porcento.](./{arquivo}-taxa-sucesso.png "Modalidade {nome_modalidade}: Taxa de Sucesso")')
        md_descritivo.write('\n')
        md_descritivo.write('\n')
        md_descritivo.write(f'Série anual. Modalidade {nome_modalidade}: Média Arrecadada.')
        md_descritivo.write('\n')
        md_descritivo.write('\n')
        md_descritivo.write(f'![Gráfico XY com o título "Modalidade {nome_modalidade}: Média Arrecadada". O eixo X é uma escala de anos. O eixo Y é uma escala valores monetários.](./{arquivo}-media-sucesso.png "Modalidade {nome_modalidade}: Média Arrecadada")')
        md_descritivo.write('\n')
        md_descritivo.write('\n')

        md_descritivo.close()

    analise_md.append({arquivo: mk_table})

    return True

# calcular a série anual de campanhas pela modalidade tudo ou nada
def gerar_serie_por_modalidade_aon(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    return _gerar_serie_por_modalidade(df, ano, comum.CAMPANHA_AON, comum.TITULOS_MODALIDADES[comum.CAMPANHA_AON], pasta_md, pasta_dados, arquivo, titulo,  template, analise_md)

# calcular a série anual de campanhas pela modalidade Flex
def gerar_serie_por_modalidade_flex(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    return _gerar_serie_por_modalidade(df, ano, comum.CAMPANHA_FLEX, comum.TITULOS_MODALIDADES[comum.CAMPANHA_FLEX], pasta_md, pasta_dados, arquivo, titulo,  template, analise_md)

# calcular a série anual de campanhas pela modalidade Recorrente
def gerar_serie_por_modalidade_sub(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    return _gerar_serie_por_modalidade(df, ano, comum.CAMPANHA_SUB, comum.TITULOS_MODALIDADES[comum.CAMPANHA_SUB], pasta_md, pasta_dados, arquivo, titulo,  template, analise_md)

# gerar o resumo de campanhas por origem e modalidades
def gerar_serie_por_origem_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    return _gerar_serie_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, colunaslib.COL_ORIGEM, analise_md)

# gerar o resumo de campanhas por uf_br
def gerar_serie_por_ufbr(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    return _gerar_serie_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, colunaslib.COL_GERAL_UF_BR, analise_md)

# gerar o resumo de campanhas por gênero
def gerar_serie_por_genero(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    return _gerar_serie_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, colunaslib.COL_AUTORIA_CLASSIFICACAO, analise_md)

# gerar o resumo de campanhas por autoria e seus respectivos status
def gerar_serie_por_autoria(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    return _gerar_serie_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, colunaslib.COL_AUTORIA_NOME_PUBLICO, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_serie_por_mencoes_angelo_agostini(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  colunaslib.COL_MENCOES_ANGELO_AGOSTINI
    return _gerar_serie_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_serie_por_mencoes_ccxp(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  colunaslib.COL_MENCOES_CCXP
    return _gerar_serie_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_serie_por_mencoes_disputa(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  colunaslib.COL_MENCOES_DISPUTA
    return _gerar_serie_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_serie_por_mencoes_erotismo(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  colunaslib.COL_MENCOES_EROTISMO
    return _gerar_serie_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_serie_por_mencoes_fantasia(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  colunaslib.COL_MENCOES_FANTASIA
    return _gerar_serie_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_serie_por_mencoes_ficcao_cientifica(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  colunaslib.COL_MENCOES_FICCAO_CIENTIFICA
    return _gerar_serie_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_serie_por_mencoes_fiq(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  colunaslib.COL_MENCOES_FIQ
    return _gerar_serie_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_serie_por_mencoes_folclore(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  colunaslib.COL_MENCOES_FOLCLORE
    return _gerar_serie_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_serie_por_mencoes_herois(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  colunaslib.COL_MENCOES_HEROIS
    return _gerar_serie_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_serie_por_mencoes_hqmix(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  colunaslib.COL_MENCOES_HQMIX
    return _gerar_serie_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_serie_por_mencoes_humor(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  colunaslib.COL_MENCOES_HUMOR
    return _gerar_serie_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_serie_por_mencoes_jogos(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  colunaslib.COL_MENCOES_JOGOS
    return _gerar_serie_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_serie_por_mencoes_lgbtqiamais(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  colunaslib.COL_MENCOES_LGBTQIAMAIS
    return _gerar_serie_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_serie_por_mencoes_midia_independente(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  colunaslib.COL_MENCOES_MIDIA_INDEPENDENTE
    return _gerar_serie_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_serie_por_mencoes_politica(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  colunaslib.COL_MENCOES_POLITICA
    return _gerar_serie_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_serie_por_mencoes_questoes_genero(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  colunaslib.COL_MENCOES_QUESTOES_GENERO
    return _gerar_serie_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_serie_por_mencoes_religiosidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  colunaslib.COL_MENCOES_RELIGIOSIDADE
    return _gerar_serie_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_serie_por_mencoes_saloes_humor(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  colunaslib.COL_MENCOES_SALOES_HUMOR
    return _gerar_serie_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_serie_por_mencoes_terror(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  colunaslib.COL_MENCOES_TERROR
    return _gerar_serie_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_serie_por_mencoes_webformatos(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  colunaslib.COL_MENCOES_WEBFORMATOS
    return _gerar_serie_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_serie_por_mencoes_zine(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  colunaslib.COL_MENCOES_ZINE
    return _gerar_serie_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)
