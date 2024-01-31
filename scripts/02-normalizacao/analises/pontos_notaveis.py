import colunas as colunaslib
import pandas as pd
import analises.analises_comum as comum
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# formatar moeda
def numero_moeda(valor, pos):
    return f'R$ {valor:,.0f}'.replace(',', '_').replace('.', ',').replace('_', '.')

# formatar porcento
def numero_porcento(valor, pos):
    valor = valor
    return f'{valor:,.1f}%'.replace(',', '_').replace('.', ',').replace('_', '.')

# formatar inteiro
def numero_inteiro(valor, pos):
    return comum.formatar_int(str(valor))

def _obter_markdown(df_resultado, dimensao_analisada, nome_coluna, coluna_valor, nome_coluna_valor):

    #df_resultado = serie.reset_index(name=coluna_valor).rename(columns={dimensao_analisada: nome_coluna}).rename(columns={coluna_valor: nome_coluna_valor})
    df_formatado = df_resultado.copy()

    for coluna in df_formatado.columns:
        if coluna.startswith('Total'):
            df_formatado[coluna] = df_formatado[coluna].map(comum.formatar_int)
        elif coluna =='Taxa de Sucesso':
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

    return mk_table

def _determinar_ranking(df, col_ranking, ranking_total):
    # Crie uma cópia do DataFrame para evitar o aviso "SettingWithCopyWarning"
    df = df.copy()
    df['pontuacao_composta'] = 1000*df[col_ranking] + df['taxa_sucesso']

    # Obter os índices dos maiores valores na pontuação composta
    top_indices_total = df.nlargest(ranking_total, 'pontuacao_composta').index

    # Filtrar o DataFrame original com base nos índices obtidos
    top_campanhas = df.loc[top_indices_total]

    return top_campanhas

def _rankear_por_modalidade(df_aon, df_flex, df_sub, col_ranking, ranking_total):
    res = {}

    res[comum.CAMPANHA_AON]  = _determinar_ranking(df_aon , col_ranking, ranking_total)
    res[comum.CAMPANHA_FLEX] = _determinar_ranking(df_flex, col_ranking, ranking_total)
    res[comum.CAMPANHA_SUB]  = _determinar_ranking(df_sub , col_ranking, ranking_total)

    res = comum.remover_colunas_apoio(res, [
        'pontuacao_composta',
    ])

    return res


def _gerar_grafico_barras_horizontais(df_resultado, col_categoria, col_valor, pasta_dados, arquivo, tipo_grafico, titulo, eixo_x, eixo_y, funcao_formatacao):
    altura_grafico = 3
    if (len(df_resultado)>5):
        altura_grafico = 6

    plt.figure(figsize=(10, altura_grafico))

    # Criar uma figura com mais espaço para o eixo y
    fig, ax = plt.subplots(figsize=(8, altura_grafico))

    # Criar um gráfico de barras horizontais
    bars = ax.barh(df_resultado[col_categoria], df_resultado[col_valor])

    #Adicionar etiquetas em cada ponto de dado
    for i, (categ, valor) in enumerate(zip(df_resultado[col_categoria], df_resultado[col_valor])):
        plt.text(valor, i, funcao_formatacao(valor, 0), ha='left', va='bottom')

    plt.title(titulo)
    plt.xlabel(eixo_y)
    plt.ylabel('categoria')

    # Usar números sem notação científica no eixo x
    formatter = FuncFormatter(funcao_formatacao)
    plt.gca().xaxis.set_major_formatter(formatter)

    # Ajustar automaticamente o layout para evitar sobreposições
    plt.tight_layout()

    plt.grid(True)

    # Salvar o gráfico como uma imagem (por exemplo, PNG)
    plt.savefig(f'{pasta_dados}/{arquivo}-{tipo_grafico}.png')

    plt.close('all')


def _gerar_texto_por_modalidades(ano, modalidades, template_modalidade, titulo_modalidade, titulo, df_modalidades, col_dim, titulo_dim, col_rank, titulo_rank, val_rank, pasta_dados, arquivo, funcao_formatacao):

    resultado = ''
    for mod in modalidades:
        with open(template_modalidade[mod], 'r', encoding='utf8') as md_total:
            template_total = md_total.read()

        texto = template_total.replace('$(modalidade)', titulo_modalidade[mod])
        texto = texto.replace('$(nome_dimensao)', titulo)
        texto = texto.replace('$(ano)', str(ano))
        texto = texto.replace('$(col_dim)', col_dim)
        texto = texto.replace('$(top)', f'{val_rank}')

        _gerar_grafico_barras_horizontais(df_modalidades[mod], col_dim, col_rank, f'{pasta_dados}/graficos', arquivo, f'{col_rank}-{mod}', f'{titulo} - {titulo_rank} - {titulo_modalidade[mod]}', col_dim, titulo_rank, funcao_formatacao)

        mk_table = _obter_markdown(df_modalidades[mod], col_dim, titulo_dim, col_rank, titulo_rank)
        resultado = f'{resultado}\n\n{texto}\n\n{mk_table}\n\n\n![Gráfico de barras horizontal com o título "{titulo} - {titulo_rank} - {titulo_modalidade[mod]}". O eixo X é a dimensão analisada, o eixo Y as categorias](./graficos/{arquivo}-{col_rank}-{mod}.png "{titulo} - {titulo_rank} - {titulo_modalidade[mod]}")\n\n'
    
    return f'## {titulo_rank}\n\n{resultado}'


# gerar os rankings de campanhas por col_dim
def gerar_ranking_por_coldim(arquivos_gerados, df, ano, pasta_md, pasta_dados, arquivo, titulo, template, col_dim, titulo_dim, ranking_total, ranking_taxasucesso, ranking_valor, ranking_media, ranking_apoiomedio, ranking_contribuicoes, ranking_contribuicoesmedias):

    df_resultado = comum._calcular_resumo_por_dim_modalidade(df, col_dim)

    # Filtrar o DataFrame para cada geral_modalidade
    df_aon = df_resultado[df_resultado[colunaslib.COL_GERAL_MODALIDADE] == comum.CAMPANHA_AON]
    df_flex = df_resultado[df_resultado[colunaslib.COL_GERAL_MODALIDADE] == comum.CAMPANHA_FLEX]
    df_sub = df_resultado[df_resultado[colunaslib.COL_GERAL_MODALIDADE] == comum.CAMPANHA_SUB]

    if ( ranking_total > 0):
        top_campanhas = _rankear_por_modalidade(df_aon, df_flex, df_sub, 'total', ranking_total)

    if (ranking_contribuicoes > 0):
        top_contribuicoes = _rankear_por_modalidade(df_aon, df_flex, df_sub, 'contribuicoes', ranking_total)

    if (ranking_taxasucesso > 0):
        top_taxa_sucesso = _rankear_por_modalidade(df_aon, df_flex, df_sub, 'taxa_sucesso', ranking_total)

    if (ranking_valor > 0):
        top_arrecadacao = _rankear_por_modalidade(df_aon, df_flex, df_sub, 'arrecadado_sucesso', ranking_total)

    if (ranking_media > 0):
        top_media = _rankear_por_modalidade(df_aon, df_flex, df_sub, 'media_sucesso', ranking_total)

    if (ranking_apoiomedio > 0):
        top_apoiomedio = _rankear_por_modalidade(df_aon, df_flex, df_sub, 'apoio_medio', ranking_total)

    if (ranking_contribuicoesmedias > 0):
        top_contribuicoesmedias = _rankear_por_modalidade(df_aon, df_flex, df_sub, 'media_contribuicoes', ranking_total)

    for mod in comum.MODALIDADES:
        arquivos_gerados.append({
            'mod': mod,
            'arquivo':f'{arquivo}-{mod}.md',
            'titulo': f'Rankings: {titulo}'
        })
        with open(f'{pasta_md}/{arquivo}-{mod}.md', 'w', encoding='utf8') as md_descritivo:
            md_descritivo.write(f'{template.replace("$(nome_dimensao)", titulo).replace("$(modalidade)", comum.TITULOS_MODALIDADES[mod])}')

            md_descritivo.write('\n')

            if ( ranking_total > 0):
                texto = _gerar_texto_por_modalidades(ano, [mod], {
                    comum.CAMPANHA_AON: 'pontos-notaveis-total.template.md',
                    comum.CAMPANHA_FLEX: 'pontos-notaveis-total.template.md',
                    comum.CAMPANHA_SUB: 'pontos-notaveis-total-recorrente.template.md',
                }, {mod: comum.TITULOS_MODALIDADES[mod]}, titulo, top_campanhas, col_dim, titulo_dim, 'total', 'Total de Campanhas', ranking_total, pasta_md, arquivo, numero_inteiro)
                md_descritivo.write(f'{texto}')

            if ( ranking_contribuicoes > 0):
                texto = _gerar_texto_por_modalidades(ano, [mod], {
                    comum.CAMPANHA_AON: 'pontos-notaveis-totalcontribuicoes.template.md',
                    comum.CAMPANHA_FLEX: 'pontos-notaveis-totalcontribuicoes.template.md',
                    comum.CAMPANHA_SUB: 'pontos-notaveis-totalcontribuicoes-recorrente.template.md',
                }, {mod: comum.TITULOS_MODALIDADES[mod]}, titulo, top_contribuicoes, col_dim, titulo_dim, 'contribuicoes', 'Total de Contribuições', ranking_contribuicoes, pasta_md, arquivo, numero_inteiro)
                md_descritivo.write(f'{texto}')

            if (ranking_taxasucesso > 0):
                texto = _gerar_texto_por_modalidades(ano, [mod], {
                    comum.CAMPANHA_AON: 'pontos-notaveis-taxa-sucesso.template.md',
                    comum.CAMPANHA_FLEX: 'pontos-notaveis-taxa-sucesso.template.md',
                    comum.CAMPANHA_SUB: 'pontos-notaveis-taxa-sucesso-recorrente.template.md',
                }, {mod: comum.TITULOS_MODALIDADES[mod]}, titulo, top_taxa_sucesso, col_dim, titulo_dim, 'taxa_sucesso', 'Taxa de Sucesso', ranking_taxasucesso, pasta_md, arquivo, numero_porcento)
                md_descritivo.write(f'{texto}')

            if (ranking_valor > 0):
                texto = _gerar_texto_por_modalidades(ano, [mod], {
                    comum.CAMPANHA_AON: 'pontos-notaveis-valor-sucesso.template.md',
                    comum.CAMPANHA_FLEX: 'pontos-notaveis-valor-sucesso.template.md',
                    comum.CAMPANHA_SUB: 'pontos-notaveis-valor-sucesso-recorrente.template.md',
                }, {mod: comum.TITULOS_MODALIDADES[mod]}, titulo, top_arrecadacao, col_dim, titulo_dim, 'arrecadado_sucesso', 'Valor Total Arrecadado', ranking_valor, pasta_md, arquivo, numero_moeda)
                md_descritivo.write(f'{texto}')

            if (ranking_media > 0):
                texto = _gerar_texto_por_modalidades(ano, [mod], {
                    comum.CAMPANHA_AON: 'pontos-notaveis-media-sucesso.template.md',
                    comum.CAMPANHA_FLEX: 'pontos-notaveis-media-sucesso.template.md',
                    comum.CAMPANHA_SUB: 'pontos-notaveis-media-sucesso-recorrente.template.md',
                }, {mod: comum.TITULOS_MODALIDADES[mod]}, titulo, top_media, col_dim, titulo_dim, 'media_sucesso', 'Valor Arrecadado Médio', ranking_media, pasta_md, arquivo, numero_moeda)
                md_descritivo.write(f'{texto}')

            if (ranking_apoiomedio > 0):
                texto = _gerar_texto_por_modalidades(ano, [mod], {
                    comum.CAMPANHA_AON: 'pontos-notaveis-mediaapoio-sucesso.template.md',
                    comum.CAMPANHA_FLEX: 'pontos-notaveis-mediaapoio-sucesso.template.md',
                    comum.CAMPANHA_SUB: 'pontos-notaveis-mediaapoio-sucesso-recorrente.template.md',
                }, {mod: comum.TITULOS_MODALIDADES[mod]}, titulo, top_apoiomedio, col_dim, titulo_dim, 'apoio_medio', 'Valor Apoiado Médio', ranking_apoiomedio, pasta_md, arquivo, numero_moeda)
                md_descritivo.write(f'{texto}')

            if (ranking_contribuicoesmedias > 0):
                texto = _gerar_texto_por_modalidades(ano, [mod], {
                    comum.CAMPANHA_AON: 'pontos-notaveis-mediacontribuicoes.template.md',
                    comum.CAMPANHA_FLEX: 'pontos-notaveis-mediacontribuicoes.template.md',
                    comum.CAMPANHA_SUB: 'pontos-notaveis-mediacontribuicoes-recorrente.template.md',
                }, {mod: comum.TITULOS_MODALIDADES[mod]}, titulo, top_contribuicoesmedias, col_dim, titulo_dim, 'media_contribuicoes', 'Média de Contribuições', ranking_contribuicoesmedias, pasta_md, arquivo, numero_inteiro)
                md_descritivo.write(f'{texto}')

            md_descritivo.close()

    return True

# gerar os rankings de campanhas por uf_br
def gerar_ranking_por_ufbr(arquivos_gerados, df, ano, pasta_md, pasta_dados, arquivo, titulo,  template):
    return gerar_ranking_por_coldim(arquivos_gerados, df, ano, pasta_md, pasta_dados, arquivo, titulo, template, colunaslib.COL_GERAL_UF_BR, 'UF', 5, 5, 5, 5, 5, 5, 5)

# gerar os rankings de campanhas por gênero
def gerar_ranking_por_genero(arquivos_gerados, df, ano, pasta_md, pasta_dados, arquivo, titulo,  template):
    return gerar_ranking_por_coldim(arquivos_gerados, df, ano, pasta_md, pasta_dados, arquivo, titulo, template, colunaslib.COL_AUTORIA_CLASSIFICACAO, 'Gênero', 5, 5, 5, 5, 5, 5, 5)

# gerar os rankings de campanhas por autoria
def gerar_ranking_por_autoria(arquivos_gerados, df, ano, pasta_md, pasta_dados, arquivo, titulo,  template):
    return gerar_ranking_por_coldim(arquivos_gerados, df, ano, pasta_md, pasta_dados, arquivo, titulo, template, colunaslib.COL_AUTORIA_NOME_PUBLICO, 'Autoria', 10, 0, 10, 10, 10, 10, 10)
