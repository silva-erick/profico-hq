import pandas as pd
import analises.analises_comum as comum
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


# gerar o resumo de campanhas por dim e modalidades
def _gerar_serie_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col_dim, analise_md):

    df_resultado = comum._calcular_serie_por_dim_modalidade(df, 'aon', col_dim)

    colunas = df_resultado.columns

    df_resultado.to_csv(f'{pasta_dados}/{arquivo}_{ano}.csv', index=False, columns=colunas, sep=';', decimal=',', encoding='utf-8-sig')

    caminho_arquivo_excel = f'{pasta_dados}/{arquivo}_{ano}.xlsx'
    formatados = {}
    formatados[f'taxa_sucesso'] = {'num_format': '0.00%'}
    formatados[f'valor_sucesso'] = {'num_format': 'R$ #,##0.00'}
    formatados[f'media_sucesso'] = {'num_format': 'R$ #,##0.00'}

    comum._gravar_excel_formatado(df_resultado, caminho_arquivo_excel, formatados)

    df_formatado = df_resultado.copy()

    for coluna in df_formatado.columns:
        if coluna.startswith('total'):
            df_formatado[coluna] = df_formatado[coluna].map(comum.formatar_int)
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
    plt.plot(df_resultado['ano'], df_resultado[col_dim], marker='o', linestyle='-')

    # Adicionar etiquetas em cada ponto de dado
    for i, (ano, valor) in enumerate(zip(df_resultado['ano'], df_resultado[col_dim])):
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


# calcular a série anual de campanhas por uma modalidade
def _gerar_serie_por_modalidade(df, ano, modalidade, nome_modalidade, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):

    col_modalidade = 'geral_modalidade'

    colunas = ['ano']
    df_resultado = df[
        df[col_modalidade] == modalidade
    ].groupby(colunas).size().reset_index(name='total')

    # estender o df com mais colunas
    for index, row in df_resultado.iterrows():
        #modalidade = row[col_modalidade]
        ano_analise = row['ano']
        total_mod = row['total']

        col_taxa_sucesso = f'taxa_sucesso'
        col_total_sucesso = f'total_sucesso'
        col_valor_arrecadado_sucesso = f'arrecadado_sucesso'

        col_media_sucesso = f'media_sucesso'

        if modalidade == 'sub':
            # 'total_mod_mencao' na modalidade com referência à 'menção' com status diferente de falha
            campanhas_mod_sucesso = df[
                (df[col_modalidade] == modalidade)
                & (df['geral_total_contribuicoes'] > 0)
                & (df['ano'] == ano_analise)
                ]
            total_mod_sucesso = len(campanhas_mod_sucesso)
            valor_mod_sucesso = campanhas_mod_sucesso['geral_arrecadado_corrigido'].sum()
        else:
            # 'total_mod_mencao' na modalidade com referência à 'menção' com status diferente de falha
            campanhas_mod_sucesso = df[
                (df['geral_modalidade'] == modalidade)
                & (df['geral_status'] != 'failed')
                & (df['ano'] == ano_analise)
                ]
            total_mod_sucesso = len(campanhas_mod_sucesso)
            valor_mod_sucesso = campanhas_mod_sucesso['geral_arrecadado_corrigido'].sum()
        
        df_resultado.at[index, col_total_sucesso] = int(total_mod_sucesso)
        df_resultado.at[index, col_valor_arrecadado_sucesso] = valor_mod_sucesso
        df_resultado.at[index, col_taxa_sucesso] = comum._dividir(total_mod_sucesso, total_mod)
        df_resultado.at[index, col_media_sucesso] = comum._dividir(valor_mod_sucesso, total_mod_sucesso)

    # Preencher NaN com 0 para evitar problemas na divisão
    df_resultado = df_resultado.fillna(0)

    df_resultado.to_csv(f'{pasta_dados}/{arquivo}_{ano}.csv', index=False, sep=';', decimal=',', encoding='utf-8-sig')

    caminho_arquivo_excel = f'{pasta_dados}/{arquivo}_{ano}.xlsx'
    comum._gravar_excel_formatado(df_resultado, caminho_arquivo_excel, {
        'taxa_sucesso': {'num_format': '0.00%'},
        'arrecadado_sucesso': {'num_format': 'R$ #,##0.00'},
        'media_sucesso': {'num_format': 'R$ #,##0.00'},
        })


    _gerar_grafico(df_resultado, 'total', pasta_md, arquivo, 'campanhas', f'Modalidade {nome_modalidade}: Total de Campanhas', 'Ano', 'Campanhas', numero_inteiro)
    _gerar_grafico(df_resultado, 'total_sucesso', pasta_md, arquivo, 'bem-sucedidas', f'Modalidade {nome_modalidade}: Total de Campanhas bem Sucedidas', 'Ano', 'Campanhas', numero_inteiro)
    _gerar_grafico(df_resultado, 'arrecadado_sucesso', pasta_md, arquivo, 'arrecadado', f'Modalidade {nome_modalidade}: Arrecadação Anual', 'Ano', 'Arrecadação', numero_moeda)
    _gerar_grafico(df_resultado, 'taxa_sucesso', pasta_md, arquivo, 'taxa-sucesso', f'Modalidade {nome_modalidade}: Taxa de Sucesso', 'Ano', 'Taxa de Sucesso', numero_porcento)
    _gerar_grafico(df_resultado, 'media_sucesso', pasta_md, arquivo, 'media-sucesso', f'Modalidade {nome_modalidade}: Média Arrecadada', 'Ano', 'Média', numero_moeda)
    
    df_formatado = df_resultado.copy()

    for coluna in df_formatado.columns:
        if coluna.startswith('total'):
            df_formatado[coluna] = df_formatado[coluna].map(comum.formatar_int)
        elif coluna == 'ano':
            df_formatado[coluna] = df_formatado[coluna].map(comum.formatar_nada)
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
    return _gerar_serie_por_modalidade(df, ano, 'aon', 'Tudo ou Nada', pasta_md, pasta_dados, arquivo, titulo,  template, analise_md)

# calcular a série anual de campanhas pela modalidade Flex
def gerar_serie_por_modalidade_flex(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    return _gerar_serie_por_modalidade(df, ano, 'flex', 'Flex', pasta_md, pasta_dados, arquivo, titulo,  template, analise_md)

# gerar o resumo de campanhas por origem e modalidades
def gerar_serie_por_origem_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    return _gerar_serie_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, 'origem', analise_md)

# gerar o resumo de campanhas por uf_br
def gerar_serie_por_ufbr(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    return _gerar_serie_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, 'geral_uf_br', analise_md)

# gerar o resumo de campanhas por gênero
def gerar_serie_por_genero(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    return _gerar_serie_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, 'autoria_classificacao', analise_md)

# gerar o resumo de campanhas por autoria e seus respectivos status
def gerar_serie_por_autoria(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    return _gerar_serie_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, 'autoria_nome_publico', analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_serie_por_mencoes_angelo_agostini(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  'mencoes_angelo_agostini'
    return _gerar_serie_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_serie_por_mencoes_ccxp(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  'mencoes_ccxp'
    return _gerar_serie_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_serie_por_mencoes_disputa(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  'mencoes_disputa'
    return _gerar_serie_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_serie_por_mencoes_erotismo(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  'mencoes_erotismo'
    return _gerar_serie_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_serie_por_mencoes_fantasia(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  'mencoes_fantasia'
    return _gerar_serie_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_serie_por_mencoes_ficcao_cientifica(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  'mencoes_ficcao_cientifica'
    return _gerar_serie_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_serie_por_mencoes_fiq(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  'mencoes_fiq'
    return _gerar_serie_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_serie_por_mencoes_folclore(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  'mencoes_folclore'
    return _gerar_serie_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_serie_por_mencoes_herois(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  'mencoes_herois'
    return _gerar_serie_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_serie_por_mencoes_hqmix(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  'mencoes_hqmix'
    return _gerar_serie_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_serie_por_mencoes_humor(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  'mencoes_humor'
    return _gerar_serie_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_serie_por_mencoes_jogos(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  'mencoes_jogos'
    return _gerar_serie_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_serie_por_mencoes_lgbtqiamais(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  'mencoes_lgbtqiamais'
    return _gerar_serie_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_serie_por_mencoes_midia_independente(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  'mencoes_midia_independente'
    return _gerar_serie_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_serie_por_mencoes_politica(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  'mencoes_politica'
    return _gerar_serie_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_serie_por_mencoes_questoes_genero(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  'mencoes_questoes_genero'
    return _gerar_serie_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_serie_por_mencoes_religiosidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  'mencoes_religiosidade'
    return _gerar_serie_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_serie_por_mencoes_saloes_humor(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  'mencoes_saloes_humor'
    return _gerar_serie_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_serie_por_mencoes_terror(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  'mencoes_terror'
    return _gerar_serie_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_serie_por_mencoes_webformatos(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  'mencoes_webformatos'
    return _gerar_serie_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)

# gerar o resumo de menção de acordo com a modalidade das campanhas
def gerar_serie_por_mencoes_zine(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, analise_md):
    col =  'mencoes_zine'
    return _gerar_serie_por_dim_modalidade(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template, col, analise_md)
