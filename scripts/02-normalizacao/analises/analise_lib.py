import pandas as pd
import re
import os
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import time
import colunas as colunaslib


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

DFCOL_META                  = 'meta'
DFCOL_META_MED              = 'meta_avg'
DFCOL_META_STD              = 'meta_std'
DFCOL_META_MIN              = 'meta_min'
DFCOL_META_MAX              = 'meta_max'

DFCOL_ARRECADADO            = 'arrecadado'
DFCOL_ARRECADADO_SUCESSO    = 'arrecadado_sucesso'
DFCOL_ARRECADADO_MED        = 'arrecadado_avg'
DFCOL_ARRECADADO_STD        = 'arrecadado_std'
DFCOL_ARRECADADO_MIN        = 'arrecadado_min'
DFCOL_ARRECADADO_MAX        = 'arrecadado_max'

DFCOL_APOIO_MED             = 'apoio_medio'
DFCOL_APOIO_STD             = 'apoio_std'
DFCOL_APOIO_MIN             = 'apoio_min'
DFCOL_APOIO_MAX             = 'apoio_max'

DFCOL_CONTRIBUICOES         = 'contribuicoes'
DFCOL_CONTRIBUICOES_MED     = 'contribuicoes_med'
DFCOL_CONTRIBUICOES_STD     = 'contribuicoes_std'
DFCOL_CONTRIBUICOES_MIN     = 'contribuicoes_min'
DFCOL_CONTRIBUICOES_MAX     = 'contribuicoes_max'

DFCOL_ORIGEM                = 'origem'
DFCOL_GENERO                = 'autoria_classificacao'
DFCOL_UF                    = 'geral_uf_br'
DFCOL_MENCAO                = 'mencao'


def marcar_andamento(deslocamento, start_time):
    print(f"{deslocamento}###> andamento: {(time.time() - start_time):.1f} segundos", flush=True)


def marcar_andamento_mesma_linha(start_time):
    print(f"{(time.time() - start_time):.1f} segundos", flush=True)

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
Formatar número com prefixos
"""
def numero_prefixo_f(string_com_numeros, pos = 0):
    str_original = string_com_numeros
    sinal = 1
    num_temp = float(string_com_numeros)
    if num_temp > 0:
        sinal = 1
    else:
        sinal = -1
        num_temp = abs(num_temp)

    num_convertido = ''
    if ( num_temp >= 1000000 ):
        num_temp = num_temp / 1000000
        num_convertido = numero_com_separadores(str(num_temp), 1) + 'M'
    elif ( num_temp >= 1000 ):
        num_temp = num_temp / 1000
        num_convertido = numero_com_separadores(str(num_temp), 1) + 'K'
    else:
        num_convertido = numero_com_separadores(str(num_temp), 0)

    if sinal > 0:
        return num_convertido
    else:
        return '-' + num_convertido

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
        num = float(num / 1000000)
        resultado = f'{num:.1f}M'
    elif num > 1000:
        num = float(num / 1000)
        resultado = f'{num:.1f}K'
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
Gerar gráfico: histograma
"""
def gerar_histograma(pasta_img, arquivo, df, bins, col_interesse, titulo, titulo_eixo_x, titulo_eixo_y, funcao_formatacao_eixo=formatar_num_eixo_y):
    
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
    formatados[comum.DFCOL_ARRECADADO_MED] = {'num_format': 'R$ #,##0.00'}
    formatados[comum.DFCOL_ARRECADADO_STD] = {'num_format': 'R$ #,##0.00'}
    formatados[comum.DFCOL_ARRECADADO_MIN] = {'num_format': 'R$ #,##0.00'}
    formatados[comum.DFCOL_ARRECADADO_MAX] = {'num_format': 'R$ #,##0.00'}
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



class CalculosDescritivos(AnaliseInterface):

    """
    Executar a análise descritiva agrupando 
    """
    def executar(self, df_completo) -> bool:

        self.df_completo                = df_completo
        self.df_resumo_mod              = self._calcular_resumo_por_modalidade(df_completo)
        self.df_resumo_mod_plataforma   = self._calcular_resumo_por_modalidade_recorte(df_completo, colunaslib.COL_ORIGEM)
        self.df_resumo_mod_uf           = self._calcular_resumo_por_modalidade_recorte(df_completo, colunaslib.COL_GERAL_UF_BR)
        self.df_resumo_mod_genero       = self._calcular_resumo_por_modalidade_recorte(df_completo, colunaslib.COL_AUTORIA_CLASSIFICACAO)
        self.df_resumo_mod_mencoes      = self._calcular_resumo_por_modalidade_mencoes(df_completo)

        return True

    """
    Obter campanhas bem sucedidas
    """
    def _obter_campanhas_bem_sucedidas(self, modalidade, df):
        if modalidade == CAMPANHA_SUB:
            campanhas_mod_sucesso = df[
                (df[colunaslib.COL_GERAL_MODALIDADE] == modalidade)
                & (df[colunaslib.COL_GERAL_TOTAL_CONTRIBUICOES] > 0)
                ]
        else:
            campanhas_mod_sucesso = df[
                (df[colunaslib.COL_GERAL_MODALIDADE] == modalidade)
                & (df[colunaslib.COL_GERAL_STATUS] != 'failed')
                ]
        
        return campanhas_mod_sucesso

    """
    calcular o resumo de indicadores das campanhas por modalidades
    """    
    def _calcular_resumo_por_modalidade(self, df_completo):
        colunas = [colunaslib.COL_GERAL_MODALIDADE]
        df_resumo = df_completo.groupby(colunas).size().reset_index(name=DFCOL_TOTAL)

        total = df_resumo[DFCOL_TOTAL].sum()

        # estender o df com mais colunas
        for index, row in df_resumo.iterrows():
            modalidade = row[colunaslib.COL_GERAL_MODALIDADE]
            total_mod = row[DFCOL_TOTAL]

            campanhas_mod_sucesso = self._obter_campanhas_bem_sucedidas(modalidade, df_completo)

            total_mod_sucesso           = len(campanhas_mod_sucesso)
            meta_mod_sucesso            = campanhas_mod_sucesso[colunaslib.COL_GERAL_META_CORRIGIDA].sum()
            meta_mod_sucesso_med        = campanhas_mod_sucesso[colunaslib.COL_GERAL_META_CORRIGIDA].mean()
            meta_mod_sucesso_std        = campanhas_mod_sucesso[colunaslib.COL_GERAL_META_CORRIGIDA].std()
            meta_mod_sucesso_min        = campanhas_mod_sucesso[colunaslib.COL_GERAL_META_CORRIGIDA].min()
            meta_mod_sucesso_max        = campanhas_mod_sucesso[colunaslib.COL_GERAL_META_CORRIGIDA].max()

            valor_mod_sucesso           = campanhas_mod_sucesso[colunaslib.COL_GERAL_ARRECADADO_CORRIGIDO].sum()
            valor_med_mod_sucesso       = campanhas_mod_sucesso[colunaslib.COL_GERAL_ARRECADADO_CORRIGIDO].mean()
            valor_std_mod_sucesso       = campanhas_mod_sucesso[colunaslib.COL_GERAL_ARRECADADO_CORRIGIDO].std()
            valor_min_mod_sucesso       = campanhas_mod_sucesso[colunaslib.COL_GERAL_ARRECADADO_CORRIGIDO].min()
            valor_max_mod_sucesso       = campanhas_mod_sucesso[colunaslib.COL_GERAL_ARRECADADO_CORRIGIDO].max()

            apoio_med_mod_sucesso       = campanhas_mod_sucesso[colunaslib.COL_GERAL_APOIO_MEDIO].mean()
            apoio_std_mod_sucesso       = campanhas_mod_sucesso[colunaslib.COL_GERAL_APOIO_MEDIO].std()
            apoio_min_mod_sucesso       = campanhas_mod_sucesso[colunaslib.COL_GERAL_APOIO_MEDIO].min()
            apoio_max_mod_sucesso       = campanhas_mod_sucesso[colunaslib.COL_GERAL_APOIO_MEDIO].max()

            contribuicoes               = campanhas_mod_sucesso[colunaslib.COL_GERAL_TOTAL_CONTRIBUICOES].sum()
            contribuicoes_med           = campanhas_mod_sucesso[colunaslib.COL_GERAL_TOTAL_CONTRIBUICOES].mean()
            contribuicoes_std           = campanhas_mod_sucesso[colunaslib.COL_GERAL_TOTAL_CONTRIBUICOES].std()
            contribuicoes_min           = campanhas_mod_sucesso[colunaslib.COL_GERAL_TOTAL_CONTRIBUICOES].min()
            contribuicoes_max           = campanhas_mod_sucesso[colunaslib.COL_GERAL_TOTAL_CONTRIBUICOES].max()

            menor_ano           = campanhas_mod_sucesso[colunaslib.COL_ANO].min()
            maior_ano           = campanhas_mod_sucesso[colunaslib.COL_ANO].max()
            
            df_resumo.at[index, DFCOL_TOTAL]                = int(total_mod)
            df_resumo.at[index, DFCOL_TOTAL_SUCESSO]        = int(total_mod_sucesso)
            df_resumo.at[index, DFCOL_PARTICIP]             = _dividir(total_mod, total)
            df_resumo.at[index, DFCOL_TAXA_SUCESSO]         = _dividir(total_mod_sucesso, total_mod)
            df_resumo.at[index, DFCOL_META]                 = meta_mod_sucesso
            df_resumo.at[index, DFCOL_META_MED]             = meta_mod_sucesso_med
            df_resumo.at[index, DFCOL_META_STD]             = meta_mod_sucesso_std
            df_resumo.at[index, DFCOL_META_MIN]             = meta_mod_sucesso_min
            df_resumo.at[index, DFCOL_META_MAX]             = meta_mod_sucesso_max
            df_resumo.at[index, DFCOL_ARRECADADO_SUCESSO]   = valor_mod_sucesso
            df_resumo.at[index, DFCOL_ARRECADADO_MED]       = valor_med_mod_sucesso
            df_resumo.at[index, DFCOL_ARRECADADO_STD]       = valor_std_mod_sucesso
            df_resumo.at[index, DFCOL_ARRECADADO_MIN]       = valor_min_mod_sucesso
            df_resumo.at[index, DFCOL_ARRECADADO_MAX]       = valor_max_mod_sucesso
            df_resumo.at[index, DFCOL_APOIO_MED]            = apoio_med_mod_sucesso
            df_resumo.at[index, DFCOL_APOIO_STD]            = apoio_std_mod_sucesso
            df_resumo.at[index, DFCOL_APOIO_MIN]            = apoio_min_mod_sucesso
            df_resumo.at[index, DFCOL_APOIO_MAX]            = apoio_max_mod_sucesso
            df_resumo.at[index, DFCOL_CONTRIBUICOES]        = contribuicoes
            df_resumo.at[index, DFCOL_CONTRIBUICOES_MED]    = contribuicoes_med
            df_resumo.at[index, DFCOL_CONTRIBUICOES_STD]    = contribuicoes_std
            df_resumo.at[index, DFCOL_CONTRIBUICOES_MIN]    = contribuicoes_min
            df_resumo.at[index, DFCOL_CONTRIBUICOES_MAX]    = contribuicoes_max
            df_resumo.at[index, DFCOL_MENOR_ANO]            = menor_ano
            df_resumo.at[index, DFCOL_MAIOR_ANO]            = maior_ano


        # Preencher NaN com 0 para evitar problemas na divisão
        df_resumo = df_resumo.fillna(0)
        df_resumo.rename(columns={colunaslib.COL_GERAL_MODALIDADE: DFCOL_MODALIDADE}, inplace=True)

        df_resumo[DFCOL_MENOR_ANO]       = df_resumo[DFCOL_MENOR_ANO].round().astype('int64')
        df_resumo[DFCOL_MAIOR_ANO]       = df_resumo[DFCOL_MAIOR_ANO].round().astype('int64')


        return df_resumo

    """
    calcular o resumo de campanhas por modalidade e recorte
    """
    def _calcular_resumo_por_modalidade_recorte(self, df_completo, col_recorte):

        col_modalidade = colunaslib.COL_GERAL_MODALIDADE

        colunas = [col_modalidade, col_recorte]
        df_resultado = df_completo.groupby(colunas).size().reset_index(name='total')

        # estender o df_completo com mais colunas
        for index, row in df_resultado.iterrows():
            recorte = row[col_recorte]
            total_recorte = row['total']
            modalidade = row[col_modalidade]

            campanhas_mod = df_completo[
                (df_completo[col_modalidade] == modalidade)
                ]
            total_mod = len(campanhas_mod)

            campanhas_recorte_mod = df_completo[
                (df_completo[col_recorte] == recorte)
                & (df_completo[col_modalidade] == modalidade)
                ]
            total_recorte_mod = len(campanhas_recorte_mod)

            campanhas_recorte_mod_sucesso = self._obter_campanhas_bem_sucedidas(modalidade, campanhas_recorte_mod)

            total_recorte_mod_sucesso       = len(campanhas_recorte_mod_sucesso)

            meta_recorte_mod_sucesso        = campanhas_recorte_mod_sucesso[colunaslib.COL_GERAL_META_CORRIGIDA].sum()
            meta_recorte_mod_sucesso_med    = campanhas_recorte_mod_sucesso[colunaslib.COL_GERAL_META_CORRIGIDA].mean()
            meta_recorte_mod_sucesso_std    = campanhas_recorte_mod_sucesso[colunaslib.COL_GERAL_META_CORRIGIDA].std()
            meta_recorte_mod_sucesso_min    = campanhas_recorte_mod_sucesso[colunaslib.COL_GERAL_META_CORRIGIDA].min()
            meta_recorte_mod_sucesso_max    = campanhas_recorte_mod_sucesso[colunaslib.COL_GERAL_META_CORRIGIDA].max()

            valor_recorte_mod_sucesso       = campanhas_recorte_mod_sucesso[colunaslib.COL_GERAL_ARRECADADO_CORRIGIDO].sum()
            valor_med_recorte_mod_sucesso   = campanhas_recorte_mod_sucesso[colunaslib.COL_GERAL_ARRECADADO_CORRIGIDO].mean()
            valor_std_recorte_mod_sucesso   = campanhas_recorte_mod_sucesso[colunaslib.COL_GERAL_ARRECADADO_CORRIGIDO].std()
            valor_min_recorte_mod_sucesso   = campanhas_recorte_mod_sucesso[colunaslib.COL_GERAL_ARRECADADO_CORRIGIDO].min()
            valor_max_recorte_mod_sucesso   = campanhas_recorte_mod_sucesso[colunaslib.COL_GERAL_ARRECADADO_CORRIGIDO].max()
            apoio_med_recorte_mod_sucesso   = campanhas_recorte_mod_sucesso[colunaslib.COL_GERAL_APOIO_MEDIO].mean()
            apoio_std_recorte_mod_sucesso   = campanhas_recorte_mod_sucesso[colunaslib.COL_GERAL_APOIO_MEDIO].std()
            apoio_min_recorte_mod_sucesso   = campanhas_recorte_mod_sucesso[colunaslib.COL_GERAL_APOIO_MEDIO].min()
            apoio_max_recorte_mod_sucesso   = campanhas_recorte_mod_sucesso[colunaslib.COL_GERAL_APOIO_MEDIO].max()
            contribuicoes                   = campanhas_recorte_mod_sucesso[colunaslib.COL_GERAL_TOTAL_CONTRIBUICOES].sum()
            contribuicoes_std               = campanhas_recorte_mod_sucesso[colunaslib.COL_GERAL_TOTAL_CONTRIBUICOES].std()
            contribuicoes_med               = campanhas_recorte_mod_sucesso[colunaslib.COL_GERAL_TOTAL_CONTRIBUICOES].mean()
            contribuicoes_min               = campanhas_recorte_mod_sucesso[colunaslib.COL_GERAL_TOTAL_CONTRIBUICOES].min()
            contribuicoes_max               = campanhas_recorte_mod_sucesso[colunaslib.COL_GERAL_TOTAL_CONTRIBUICOES].max()
            menor_ano                       = campanhas_recorte_mod_sucesso[colunaslib.COL_ANO].min()
            maior_ano                       = campanhas_recorte_mod_sucesso[colunaslib.COL_ANO].max()

            df_resultado.at[index, DFCOL_TOTAL]                 = int(total_recorte_mod)
            df_resultado.at[index, DFCOL_TOTAL_SUCESSO]         = int(total_recorte_mod_sucesso)
            df_resultado.at[index, DFCOL_PARTICIP]              = _dividir(total_recorte_mod, total_mod)
            df_resultado.at[index, DFCOL_TAXA_SUCESSO]          = _dividir(total_recorte_mod_sucesso, total_recorte_mod)
            
            df_resultado.at[index, DFCOL_META]                  = meta_recorte_mod_sucesso
            df_resultado.at[index, DFCOL_META_MED]              = meta_recorte_mod_sucesso_med
            df_resultado.at[index, DFCOL_META_STD]              = meta_recorte_mod_sucesso_std
            df_resultado.at[index, DFCOL_META_MIN]              = meta_recorte_mod_sucesso_min
            df_resultado.at[index, DFCOL_META_MAX]              = meta_recorte_mod_sucesso_max

            df_resultado.at[index, DFCOL_ARRECADADO_SUCESSO]    = valor_recorte_mod_sucesso
            df_resultado.at[index, DFCOL_ARRECADADO_MED]        = valor_med_recorte_mod_sucesso
            df_resultado.at[index, DFCOL_ARRECADADO_STD]        = valor_std_recorte_mod_sucesso
            df_resultado.at[index, DFCOL_ARRECADADO_MIN]        = valor_min_recorte_mod_sucesso
            df_resultado.at[index, DFCOL_ARRECADADO_MAX]        = valor_max_recorte_mod_sucesso
            df_resultado.at[index, DFCOL_APOIO_MED]             = apoio_med_recorte_mod_sucesso
            df_resultado.at[index, DFCOL_APOIO_STD]             = apoio_std_recorte_mod_sucesso
            df_resultado.at[index, DFCOL_APOIO_MIN]             = apoio_min_recorte_mod_sucesso
            df_resultado.at[index, DFCOL_APOIO_MAX]             = apoio_max_recorte_mod_sucesso
            df_resultado.at[index, DFCOL_CONTRIBUICOES]         = contribuicoes
            df_resultado.at[index, DFCOL_CONTRIBUICOES_MED]     = contribuicoes_med
            df_resultado.at[index, DFCOL_CONTRIBUICOES_STD]     = contribuicoes_std
            df_resultado.at[index, DFCOL_CONTRIBUICOES_MIN]     = contribuicoes_min
            df_resultado.at[index, DFCOL_CONTRIBUICOES_MAX]     = contribuicoes_max
            df_resultado.at[index, DFCOL_MENOR_ANO]             = menor_ano
            df_resultado.at[index, DFCOL_MAIOR_ANO]             = maior_ano

        # Preencher NaN com 0 para evitar problemas na divisão
        df_resultado = df_resultado.fillna(0)

        # garantir colunas int64:
        df_resultado[DFCOL_TOTAL]           = df_resultado[DFCOL_TOTAL].round().astype('int64')
        df_resultado[DFCOL_TOTAL_SUCESSO]   = df_resultado[DFCOL_TOTAL_SUCESSO].round().astype('int64')
        df_resultado[DFCOL_CONTRIBUICOES]   = df_resultado[DFCOL_CONTRIBUICOES].round().astype('int64')

        df_resultado[DFCOL_MENOR_ANO]       = df_resultado[DFCOL_MENOR_ANO].round().astype('int64')
        df_resultado[DFCOL_MAIOR_ANO]       = df_resultado[DFCOL_MAIOR_ANO].round().astype('int64')

        df_resultado.rename(columns={colunaslib.COL_GERAL_MODALIDADE: DFCOL_MODALIDADE}, inplace=True)

        return df_resultado

    """
    reestruturar um dataframe de menções, ignorando as linhas de True para a
    coluna analisada
    """
    def _reestruturar_df_mencoes(self, df_parcial, col):
        df_resultado = df_parcial[
            df_parcial[col]==True
        ].copy()
        df_resultado.rename(columns={col: 'mencao'}, inplace=True)
        df_resultado['mencao'] = col.replace('mencoes_', '')

        return df_resultado

    """
    calcular o resumo de campanhas por modalidade e menções
    """
    def _calcular_resumo_por_modalidade_mencoes(self, df_completo):
        
        df_angelo   =  self._reestruturar_df_mencoes(self._calcular_resumo_por_modalidade_recorte(df_completo, colunaslib.COL_MENCOES_ANGELO_AGOSTINI), colunaslib.COL_MENCOES_ANGELO_AGOSTINI)
        df_ccxp     =  self._reestruturar_df_mencoes(self._calcular_resumo_por_modalidade_recorte(df_completo, colunaslib.COL_MENCOES_CCXP), colunaslib.COL_MENCOES_CCXP)
        df_disputa  =  self._reestruturar_df_mencoes(self._calcular_resumo_por_modalidade_recorte(df_completo, colunaslib.COL_MENCOES_DISPUTA), colunaslib.COL_MENCOES_DISPUTA)
        df_erotismo =  self._reestruturar_df_mencoes(self._calcular_resumo_por_modalidade_recorte(df_completo, colunaslib.COL_MENCOES_EROTISMO), colunaslib.COL_MENCOES_EROTISMO)
        df_fantasia =  self._reestruturar_df_mencoes(self._calcular_resumo_por_modalidade_recorte(df_completo, colunaslib.COL_MENCOES_FANTASIA), colunaslib.COL_MENCOES_FANTASIA)
        df_fc       =  self._reestruturar_df_mencoes(self._calcular_resumo_por_modalidade_recorte(df_completo, colunaslib.COL_MENCOES_FICCAO_CIENTIFICA), colunaslib.COL_MENCOES_FICCAO_CIENTIFICA)
        df_fiq      =  self._reestruturar_df_mencoes(self._calcular_resumo_por_modalidade_recorte(df_completo, colunaslib.COL_MENCOES_FIQ), colunaslib.COL_MENCOES_FIQ)
        df_folclore =  self._reestruturar_df_mencoes(self._calcular_resumo_por_modalidade_recorte(df_completo, colunaslib.COL_MENCOES_FOLCLORE), colunaslib.COL_MENCOES_FOLCLORE)
        df_herois   =  self._reestruturar_df_mencoes(self._calcular_resumo_por_modalidade_recorte(df_completo, colunaslib.COL_MENCOES_HEROIS), colunaslib.COL_MENCOES_HEROIS)
        df_hqmix    =  self._reestruturar_df_mencoes(self._calcular_resumo_por_modalidade_recorte(df_completo, colunaslib.COL_MENCOES_HQMIX), colunaslib.COL_MENCOES_HQMIX)
        df_humor    =  self._reestruturar_df_mencoes(self._calcular_resumo_por_modalidade_recorte(df_completo, colunaslib.COL_MENCOES_HQMIX), colunaslib.COL_MENCOES_HQMIX)
        df_jogos    =  self._reestruturar_df_mencoes(self._calcular_resumo_por_modalidade_recorte(df_completo, colunaslib.COL_MENCOES_JOGOS), colunaslib.COL_MENCOES_JOGOS)
        df_lgbt     =  self._reestruturar_df_mencoes(self._calcular_resumo_por_modalidade_recorte(df_completo, colunaslib.COL_MENCOES_LGBTQIAMAIS), colunaslib.COL_MENCOES_LGBTQIAMAIS)
        df_midia    =  self._reestruturar_df_mencoes(self._calcular_resumo_por_modalidade_recorte(df_completo, colunaslib.COL_MENCOES_MIDIA_INDEPENDENTE), colunaslib.COL_MENCOES_MIDIA_INDEPENDENTE)
        df_politica =  self._reestruturar_df_mencoes(self._calcular_resumo_por_modalidade_recorte(df_completo, colunaslib.COL_MENCOES_POLITICA), colunaslib.COL_MENCOES_POLITICA)
        df_questoes =  self._reestruturar_df_mencoes(self._calcular_resumo_por_modalidade_recorte(df_completo, colunaslib.COL_MENCOES_QUESTOES_GENERO), colunaslib.COL_MENCOES_QUESTOES_GENERO)
        df_religiao =  self._reestruturar_df_mencoes(self._calcular_resumo_por_modalidade_recorte(df_completo, colunaslib.COL_MENCOES_RELIGIOSIDADE), colunaslib.COL_MENCOES_RELIGIOSIDADE)
        df_saloes   =  self._reestruturar_df_mencoes(self._calcular_resumo_por_modalidade_recorte(df_completo, colunaslib.COL_MENCOES_SALOES_HUMOR), colunaslib.COL_MENCOES_SALOES_HUMOR)
        df_terror   =  self._reestruturar_df_mencoes(self._calcular_resumo_por_modalidade_recorte(df_completo, colunaslib.COL_MENCOES_TERROR), colunaslib.COL_MENCOES_TERROR)
        df_web      =  self._reestruturar_df_mencoes(self._calcular_resumo_por_modalidade_recorte(df_completo, colunaslib.COL_MENCOES_WEBFORMATOS), colunaslib.COL_MENCOES_WEBFORMATOS)
        df_zine     =  self._reestruturar_df_mencoes(self._calcular_resumo_por_modalidade_recorte(df_completo, colunaslib.COL_MENCOES_ZINE), colunaslib.COL_MENCOES_ZINE)

        df_resultado = pd.concat([
            df_angelo
            ,df_ccxp
            ,df_disputa
            ,df_erotismo
            ,df_fantasia
            ,df_fc
            ,df_fiq
            ,df_folclore
            ,df_herois
            ,df_hqmix
            ,df_humor
            ,df_jogos
            ,df_lgbt
            ,df_midia
            ,df_politica
            ,df_questoes
            ,df_religiao
            ,df_saloes
            ,df_terror
            ,df_web
            ,df_zine
        ], ignore_index=True)

        return df_resultado
