import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import math
import arquivos
import pandas as pd


CAMINHO_SQL = "./analise/sql"
CAMINHO_ANALISES = "../dados/analises"
CAMINHO_NORMALIZADOS = "../dados/normalizados"

CAMINHO_SCRIPTS_ANALISES = "./analise/scripts"

CAMINHO_SQL_ANALISES_SERIES = "./analise/scripts/03-series"

class SqlLote:
    """
    Resultado de uma execução de script SQL em lote:
    - arquivo_sql
    - nome_aba
    - df
    """
    def __init__(self, arquivo_sql, nome_aba, df):
        self.arquivo_sql = arquivo_sql
        self.nome_aba = nome_aba
        self.df = df


def executar_sql_lote(con, caminho_scripts, mapa_sql={}):
    """
    Executa SQL em lote
    """

    result = {}
    for arquivo_sql,nome_aba in mapa_sql.items():
        sql = arquivos.ler_arquivo(f'{caminho_scripts}/{arquivo_sql}')
        res = con.sql(sql)
        df = res.to_df()

        item = SqlLote(arquivo_sql, nome_aba, df)

        result[arquivo_sql] = item
        #result.append(item)

    return result


def gerar_excel_lote(caminho_excel, lote={}):
    """
    gerar excel
    """

    with pd.ExcelWriter(caminho_excel) as writer:
        for chave, item in lote.items():
            item.df.to_excel(writer, sheet_name=item.nome_aba, index=False)

def formatar_num_eixo_y(num_unknown, pos=0):
    """
    formatar número para eixo y: usar prefixo K e M
    """
    if isinstance(num_unknown, str):
        num = float(num_unknown)
    elif isinstance(num_unknown, int):
        num = float(num_unknown)
    else:
        num = num_unknown

    if num > 1000000:
        num = float(num / 1000000)
        resultado = f'{num:.1f}M'
    elif num > 1000:
        num = float(num / 1000)
        resultado = f'{num:.1f}K'
    elif math.isnan(num):
        num = 0
        resultado = f'{num}'
    else:
        num = int(num)
        resultado = f'{num}'

    return resultado.replace('.', ',')


def gerar_grafico_barras(pasta_img, arquivo, df, col_x, col_y, titulo_grafico, titulo_eixo_x, titulo_eixo_y, figsize, funcao_formatacao=formatar_num_eixo_y):
    """
    gerar gráfico de barras
    """

    plt.figure(figsize=figsize)

    plt.bar(df[col_x], df[col_y])

    # Adicionar etiquetas em cada ponto de dado
    for i, (ano, valor) in enumerate(zip(df[col_x], df[col_y])):
        plt.text(ano, valor, funcao_formatacao(valor, 0), ha='left', va='bottom')

    plt.title(titulo_grafico)
    plt.xlabel(titulo_eixo_x)
    plt.ylabel(titulo_eixo_y)

    # Usar números sem notação científica no eixo y
    formatter = FuncFormatter(funcao_formatacao)
    plt.gca().yaxis.set_major_formatter(formatter)

    plt.grid(True)

    # Salvar o gráfico como uma imagem (por exemplo, PNG)
    plt.savefig(f'{pasta_img}/{arquivo}')

    plt.close('all')


# Function to add labels above the bars
def autolabel(ax, rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


def gerar_grafico_barras_2series(pasta_img, arquivo, df, col_x, col_y1, col_y2, titulo_grafico, titulo_eixo_x, titulo_eixo_y, label_serie_1, label_serie_2, figsize, funcao_formatacao=formatar_num_eixo_y):
    """
    Gerar gráfico de barras - 2 series
    """

    # Positions for the bars
    x = np.arange(len(df[col_x]))  # the label locations
    width = 0.35  # the width of the bars

    # Create the plot
    fig, ax = plt.subplots(figsize=figsize)


    # Plot the first series
    rects1 = ax.bar(x - width/2, df[col_y1], width, label=label_serie_1)

    # Plot the second series, shifted to the right
    rects2 = ax.bar(x + width/2, df[col_y2], width, label=label_serie_2)

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel(titulo_eixo_y)
    ax.set_xlabel(titulo_eixo_x)
    ax.set_title(titulo_grafico)
    ax.set_xticks(x)
    ax.set_xticklabels(df[col_x])
    ax.legend()


    autolabel(ax, rects1)
    autolabel(ax, rects2)

    # Automatically adjust subplot parameters to give specified padding
    fig.tight_layout()

    plt.grid(True)

    # Salvar o gráfico como uma imagem (por exemplo, PNG)
    plt.savefig(f'{pasta_img}/{arquivo}')

    plt.close('all')


def gerar_grafico_barras_horizontais(pasta_img, arquivo, df, col_x, col_y1, titulo, titulo_eixo_x, titulo_eixo_y, legenda_y1, funcao_formatacao, funcao_formatacao_eixo=formatar_num_eixo_y):
    """
    Gerar gráfico de barras
    """

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
    plt.savefig(f'{pasta_img}/{arquivo}', bbox_inches='tight')

    plt.close('all')


def gerar_grafico_barras_horizontais2y(pasta_img, arquivo, df, col_x, col_y1, col_y2, titulo, titulo_eixo_x, titulo_eixo_y, legenda_y1, legenda_y2, funcao_formatacao, funcao_formatacao_eixo=formatar_num_eixo_y):
    """
    Gerar gráfico de barras 2Y
    """

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
    plt.savefig(f'{pasta_img}/{arquivo}', bbox_inches='tight')

    plt.close('all')


def gerar_histograma(pasta_img, arquivo, df, bins, col_interesse, titulo, titulo_eixo_x, titulo_eixo_y, funcao_formatacao_eixo=formatar_num_eixo_y):
    """
    Gerar gráfico: histograma
    """
    
    ax = df.hist(column=col_interesse, bins=bins)

    plt.title(titulo)
    plt.xlabel(titulo_eixo_y)
    plt.ylabel(titulo_eixo_x)

    # Usar números sem notação científica no eixo x
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