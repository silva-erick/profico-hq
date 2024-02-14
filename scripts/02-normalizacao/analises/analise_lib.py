import pandas as pd
import re
import os
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


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

ORIGEM_CATARSE              = 'catarse'
ORIGEM_APOIASE              = 'apoia.se'
ORIGENS                     = [ORIGEM_CATARSE, ORIGEM_APOIASE]
TITULOS_ORIGENS = {
    ORIGEM_CATARSE : 'Catarse',
    ORIGEM_APOIASE : 'Apoia.se'
}
TITULOS_ORIGENS_LOWER = {
    ORIGEM_CATARSE : 'catarse',
    ORIGEM_APOIASE : 'apoia.se'
}

DFCOL_ORIGEM                = 'origem'
DFCOL_MODALIDADE            = 'modalidade'
DFCOL_MENOR_ANO             = 'menor_ano'
DFCOL_MAIOR_ANO             = 'maior_ano'
DFCOL_ANO                   = 'ano'
DFCOL_TOTAL                 = 'total'
DFCOL_TOTAL_SUCESSO         = 'total_sucesso'
DFCOL_TOTAL_FALHA           = 'total_falha'
DFCOL_PARTICIP              = 'particip'
DFCOL_TAXA_SUCESSO          = 'taxa_sucesso'
DFCOL_ARRECADADO            = 'arrecadado'
DFCOL_ARRECADADO_SUCESSO    = 'arrecadado_sucesso'
DFCOL_MEDIA_SUCESSO         = 'media_sucesso'
DFCOL_STD_SUCESSO           = 'std_sucesso'
DFCOL_MIN_SUCESSO           = 'min_sucesso'
DFCOL_MAX_SUCESSO           = 'max_sucesso'
DFCOL_APOIO_MEDIO           = 'apoio_medio'
DFCOL_CONTRIBUICOES         = 'contribuicoes'
DFCOL_MEDIA_CONTRIBUICOES   = 'media_contribuicoes'

DFCOL_ORIGEM                = 'origem'
DFCOL_GENERO                = 'autoria_classificacao'
DFCOL_UF                    = 'geral_uf_br'
DFCOL_MENCAO                = 'mencao'


"""
divide dois números, mas se o divisor for zero, apenas retorna zero
""" 
def _dividir(dividendo, divisor):
    if divisor == 0:
        return 0
    return dividendo / divisor

"""
enumerar strings por extenso
"""
def enumerar_strings(strings):
    length = len(strings)
    
    if length == 0:
        return ''
    elif length == 1:
        return strings[0]
    elif length == 2:
        return f'{strings[0]} e {strings[1]}'
    else:
        enumerated_strings = ', '.join(strings[:-1])
        return f'{enumerated_strings} e {strings[-1]}'

"""
Formatar números com casas
"""
def numero_com_casas(valor, casas = None):
    if isinstance(valor, str):
        valor_float = float(valor)
    else:
        valor_float = valor

    if casas is None:
        casas = 0

    if casas == 0:
        return f'{valor_float:.0f}'
    elif casas == 1:
        return f'{valor_float:.1f}'
    elif casas == 2:
        return f'{valor_float:.2f}'
    return f'{valor_float:.3f}'

def garantir_pasta(pasta)-> str:
    if not os.path.exists(pasta):
        os.mkdir(pasta)

    return pasta

"""
Formatar número com separadores
"""
def numero_com_separadores(string_com_numeros, casas = None):
    string_com_numeros = numero_com_casas(string_com_numeros, casas) + ' '
    
    # Aplicar a formatação com milhares para números com zero ou duas casas decimais
    string_com_numeros = re.sub(r'(\d)(?=(\d{3})+(\.\d{0,3})?\s)', r'\1,', string_com_numeros)

    # Trocar ponto por vírgula e vírgula por ponto para números com zero ou duas casas decimais
    string_com_numeros = re.sub(r'[\+\-]{0,1}(\d{1,3}((,\d{3})+)?(\.\d{0,3})?)', lambda x: x.group().replace('.', 'TEMPORARY_DOT').replace(',', '.').replace('TEMPORARY_DOT', ','), string_com_numeros)

    string_com_numeros = string_com_numeros.replace(' ', '')

    return string_com_numeros

"""
Formatar número inteiro com separadores
"""
def numero_inteiro_f(string_com_numeros, pos = 0):
    return numero_com_separadores(string_com_numeros, 0)

"""
Formatar percentual com 1casa
"""
def numero_percent1_f(string_com_numeros, pos = 0):
    val = 100*float(string_com_numeros)
    return f'{val:.1f}'.replace('.', ',') + '%'

"""
Formatar valor real com 1casa
"""
def numero_real1_f(string_com_numeros, pos = 0):
    return numero_com_separadores(string_com_numeros, 1)

"""
Formatar valor real com 2casa
"""
def numero_real2_f(string_com_numeros, pos = 0):
    return numero_com_separadores(string_com_numeros, 2)


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
    string_com_numeros = re.sub(r'(\d)(?=(\d{3})+(\.\d{0,3})?\s)', r'\1,', string_com_numeros)

    # Trocar ponto por vírgula e vírgula por ponto para números com zero ou duas casas decimais
    string_com_numeros = re.sub(r'[\+\-]{0,1}(\d{1,3}((,\d{3})+)?(\.\d{0,3})?)', lambda x: x.group().replace('.', 'TEMPORARY_DOT').replace(',', '.').replace('TEMPORARY_DOT', ','), string_com_numeros)

    string_com_numeros = re.sub(r'!(\d+)!', r' \1 ', string_com_numeros)


    return string_com_numeros

def formatar_percent_eixo_y(num_unknown, pos=0):
    return formatar_num_eixo_y(round(100*num_unknown, 0), pos).replace(',0', '')+'%'

def formatar_num_eixo_y(num_unknown, pos=0):
    if isinstance(num_unknown, str):
        num = float(num_unknown)
    elif isinstance(num_unknown, int):
        num = float(num_unknown)
    else:
        num = num_unknown

    if num > 1000000:
        num = int(num / 1000000)
        resultado = f'{num}M'
    elif num > 1000:
        num = int(num / 1000)
        resultado = f'{num}K'
    else:
        num = int(num)
        resultado = f'{num}'

    return resultado.replace('.', ',')

"""
Gear gráfico de barras
"""
def _gerar_grafico_barras(pasta_img, arquivo, df, col_x, col_y, legenda, titulo_eixo_x, titulo_eixo_y, funcao_formatacao):

    plt.figure(figsize=(10, 6))
    plt.plot(df[col_x], df[col_y], marker='o', linestyle='-')

    # Adicionar etiquetas em cada ponto de dado
    for i, (ano, valor) in enumerate(zip(df[col_x], df[col_y])):
        plt.text(ano, valor, funcao_formatacao(valor, 0), ha='left', va='bottom')

    plt.title(legenda)
    plt.xlabel(titulo_eixo_x)
    plt.ylabel(titulo_eixo_y)

    # Usar números sem notação científica no eixo y
    formatter = FuncFormatter(funcao_formatacao)
    plt.gca().yaxis.set_major_formatter(formatter)

    plt.grid(True)

    # Salvar o gráfico como uma imagem (por exemplo, PNG)
    plt.savefig(f'{pasta_img}/{arquivo}.png')

    plt.close('all')

"""
Gerar gráfico de barras
"""
def _gerar_grafico_barras_horizontais(pasta_img, arquivo, df, col_x, col_y1, titulo, titulo_eixo_x, titulo_eixo_y, legenda_y1, funcao_formatacao, funcao_formatacao_eixo=formatar_num_eixo_y):

    altura_grafico = round(len(df)*0.6)
    if altura_grafico < 2:
        altura_grafico = 2

    plt.figure(figsize=(10, altura_grafico))

    # Criar uma figura com mais espaço para o eixo y
    fig, ax = plt.subplots(figsize=(8, altura_grafico))

    bar_width = 0.60
    index = range(len(df))

    # Criar um gráfico de barras horizontais
    bar1 = ax.barh(index, df[col_y1], bar_width, label=legenda_y1)

    ax.set_yticks([i + bar_width / 2 for i in index])
    ax.set_yticklabels(df[col_x])

    ax.legend()

    #Adicionar etiquetas em cada ponto de dado
    for i, (categ, valor) in enumerate(zip(df[col_x], df[col_y1])):
        #plt.text(valor, i, funcao_formatacao(valor, 0), ha='left', va='top')
        ax.annotate(funcao_formatacao(valor, 0),
                    xy=(valor, i),
                    xytext=(3, 3),  # ajuste opcional para posicionamento
                    textcoords="offset points",
                    ha='left', va='top')

    plt.title(titulo)
    plt.xlabel(titulo_eixo_y)
    plt.ylabel(titulo_eixo_x)

    # Usar números sem notação científica no eixo x
    #formatter = FuncFormatter(funcao_formatacao)
    formatter = FuncFormatter(funcao_formatacao_eixo)
    plt.gca().xaxis.set_major_formatter(formatter)

    # Ajustar automaticamente o layout para evitar sobreposições
    plt.tight_layout()
    
    # Posicionar a legenda fora da área de desenho do gráfico
    plt.legend(bbox_to_anchor=(1.05, 1), loc='lower left')

    plt.grid(True)

    # Salvar o gráfico como uma imagem (por exemplo, PNG)
    plt.savefig(f'{pasta_img}/{arquivo}.png', bbox_inches='tight')

    plt.close('all')

"""
Gerar gráfico de barras 2Y
"""
def _gerar_grafico_barras_horizontais2y(pasta_img, arquivo, df, col_x, col_y1, col_y2, titulo, titulo_eixo_x, titulo_eixo_y, legenda_y1, legenda_y2, funcao_formatacao, funcao_formatacao_eixo=formatar_num_eixo_y):

    altura_grafico = round(len(df)*1)
    if altura_grafico < 2:
        altura_grafico = 2

    plt.figure(figsize=(10, altura_grafico))

    # Criar uma figura com mais espaço para o eixo y
    fig, ax = plt.subplots(figsize=(8, altura_grafico))

    bar_width = 0.35
    index = range(len(df))

    # Criar um gráfico de barras horizontais
    bar1 = ax.barh(index, df[col_y1], bar_width, label=legenda_y1)
    bar2 = ax.barh([i + bar_width for i in index], df[col_y2], bar_width, label=legenda_y2)

    ax.set_yticks([i + bar_width / 2 for i in index])
    ax.set_yticklabels(df[col_x])

    ax.legend()

    #Adicionar etiquetas em cada ponto de dado
    for i, (categ, valor) in enumerate(zip(df[col_x], df[col_y1])):
        #plt.text(valor, i, funcao_formatacao(valor, 0), ha='left', va='top')
        ax.annotate(funcao_formatacao(valor, 0),
                    xy=(valor, i),
                    xytext=(3, 3),  # ajuste opcional para posicionamento
                    textcoords="offset points",
                    ha='left', va='top')
    for i, (categ, valor) in enumerate(zip(df[col_x], df[col_y2])):
        #plt.text(valor, i, funcao_formatacao(valor, 0), ha='right', va='top')
        ax.annotate(funcao_formatacao(valor, 0),
            xy=(valor, i + bar_width),
            xytext=(3, 3),  # ajuste opcional para posicionamento
            textcoords="offset points",
            ha='left', va='top')

    plt.title(titulo)
    plt.xlabel(titulo_eixo_y)
    plt.ylabel(titulo_eixo_x)

    # Usar números sem notação científica no eixo x
    #formatter = FuncFormatter(funcao_formatacao)
    formatter = FuncFormatter(funcao_formatacao_eixo)
    plt.gca().xaxis.set_major_formatter(formatter)

    # Ajustar automaticamente o layout para evitar sobreposições
    plt.tight_layout()
    
    # Posicionar a legenda fora da área de desenho do gráfico
    plt.legend(bbox_to_anchor=(1.05, 1), loc='lower left')

    plt.grid(True)

    # Salvar o gráfico como uma imagem (por exemplo, PNG)
    plt.savefig(f'{pasta_img}/{arquivo}.png', bbox_inches='tight')

    plt.close('all')



"""
Contrato básico para as classes de análise
"""
class AnaliseInterface:
    """
    Executar
    """
    def executar(df) -> bool:
        pass

"""
Geração de arquivo CSV a partir de um dataframe do pandas
"""
class GeracaoCsv:
    """
    Gerar CSV:
    - df: dataframe do pandas
    - nome_arquivo: nome do arquivo contendo caminho de pastas absoluto ou relativo
    - colunas: lista de colunas
    """
    def executar(df, nome_arquivo, colunas=None) -> bool:
        if colunas == None:
            colunas = df.columns

        df.to_csv(nome_arquivo, index=False, columns=colunas, sep=';', decimal=',', encoding='utf-8-sig')

        return True

"""
Geração de arquivo Excel a partir de um dataframe do pandas
"""
class GeracaoExcel:
    """
    Gerar Excel
    - df: dataframe do pandas
    - nome_arquivo: nome do arquivo contendo caminho de pastas absoluto ou relativo
    - colunas_formato: lista de colunas

    Exemplos:
    formatados = {}
    formatados[comum.DFCOL_PARTICIP] = {'num_format': '0.00%'}
    formatados[comum.DFCOL_TAXA_SUCESSO] = {'num_format': '0.00%'}
    formatados[comum.DFCOL_ARRECADADO_SUCESSO] = {'num_format': 'R$ #,##0.00'}
    formatados[comum.DFCOL_MEDIA_SUCESSO] = {'num_format': 'R$ #,##0.00'}
    formatados[comum.DFCOL_STD_SUCESSO] = {'num_format': 'R$ #,##0.00'}
    formatados[comum.DFCOL_MIN_SUCESSO] = {'num_format': 'R$ #,##0.00'}
    formatados[f'max_sucesso'] = {'num_format': 'R$ #,##0.00'}
    """
    def executar(df, nome_arquivo, colunas_formato=None) -> bool:
        #comum._gravar_excel_formatado(df_resultado, caminho_arquivo_excel, formatados)

        if colunas_formato is None:
            colunas_formato = {}

        # Cria um escritor Excel
        with pd.ExcelWriter(nome_arquivo, engine='xlsxwriter') as writer:
            # Salva o DataFrame no Excel
            df.to_excel(writer, sheet_name='Sheet1', index=False)

            # Obtém o objeto de planilha
            planilha = writer.sheets['Sheet1']

            # Aplica o formato percentual às colunas
            for coluna, formato_excel in colunas_formato.items():
                if coluna in df.columns:
                    col_idx = df.columns.get_loc(coluna)
                    planilha.set_column(col_idx, col_idx, cell_format=writer.book.add_format(formato_excel))

        return True
