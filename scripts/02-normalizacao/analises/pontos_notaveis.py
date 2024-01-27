import pandas as pd
import analises.analises_comum as comum

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

def _gerar_texto(ano, caminho_arquivo_template, modalidade, titulo, df, col_dim, titulo_dim, col_rank, titulo_rank):
    with open(caminho_arquivo_template, 'r', encoding='utf8') as md_total:
        template_total = md_total.read()

    texto = template_total.replace('$(modalidade)', modalidade)
    texto = texto.replace('$(nome_dimensao)', titulo)
    texto = texto.replace('$(ano)', str(ano))

    resultado = f'{texto}\n'
    mk_table = _obter_markdown(df, col_dim, titulo_dim, col_rank, titulo_rank)
    resultado = f'{resultado}{mk_table}\n\n'
    
    return resultado

def _converter_para_df(df, serie, col_dim, col_ranking, total):

    res = []
    for index, data in serie.items():
        it = {}

        for key, row in df[df[col_dim]==index].iterrows():
            for c in df.columns:
                it[c] = row[c]

        res.append(it)

    return pd.DataFrame(res)

# gerar os rankings de campanhas por col_dim
def gerar_ranking_por_coldim(df, ano, pasta_md, pasta_dados, arquivo, titulo, template, col_dim, titulo_dim, top_total, top_taxasucesso, top_valor):

    mod_aon = 'Tudo ou Nada'
    mod_flex = 'Flex'
    mod_sub = 'Recorrente'

    df_resultado = comum._calcular_resumo_por_dim_modalidade(df, col_dim)

    # Filtrar o DataFrame para cada geral_modalidade
    df_aon = df_resultado[df_resultado['geral_modalidade'] == 'aon']
    total_aon = df_aon['total'].sum()

    df_flex = df_resultado[df_resultado['geral_modalidade'] == 'flex']
    total_flex = len(df_flex)

    df_sub = df_resultado[df_resultado['geral_modalidade'] == 'sub']
    total_sub = len(df_sub)

    # Top 5 das UF com mais campanhas realizadas para cada geral_modalidade
    top_campanhas_aon = df_aon.groupby(col_dim)['total'].mean().nlargest(top_total)
    top_campanhas_aon = _converter_para_df(df_aon, top_campanhas_aon, col_dim, 'total', total_aon)
    top_campanhas_flex = df_flex.groupby(col_dim)['total'].mean().nlargest(top_total)
    top_campanhas_flex = _converter_para_df(df_flex, top_campanhas_flex, col_dim, 'total', total_flex)
    top_campanhas_sub = df_sub.groupby(col_dim)['total'].mean().nlargest(top_total)
    top_campanhas_sub = _converter_para_df(df_sub, top_campanhas_sub, col_dim, 'total', total_sub)

    # Top 5 das UF com maiores taxas de sucesso para cada geral_modalidade
    top_taxa_sucesso_aon = df_aon.groupby(col_dim)['taxa_sucesso'].mean().nlargest(top_taxasucesso)
    top_taxa_sucesso_aon = _converter_para_df(df_aon, top_taxa_sucesso_aon, col_dim, 'total', total_aon)
    top_taxa_sucesso_flex = df_flex.groupby(col_dim)['taxa_sucesso'].mean().nlargest(top_taxasucesso)
    top_taxa_sucesso_flex = _converter_para_df(df_flex, top_taxa_sucesso_flex, col_dim, 'total', total_flex)
    top_taxa_sucesso_sub = df_sub.groupby(col_dim)['taxa_sucesso'].mean().nlargest(top_taxasucesso)
    top_taxa_sucesso_sub = _converter_para_df(df_sub, top_taxa_sucesso_sub, col_dim, 'total', total_sub)

    # Top 5 das UF com maior arrecadação para cada geral_modalidade
    top_arrecadacao_aon = df_aon.groupby(col_dim)['arrecadado_sucesso'].sum().nlargest(top_valor)
    top_arrecadacao_aon = _converter_para_df(df_aon, top_arrecadacao_aon, col_dim, 'total', total_aon)
    top_arrecadacao_flex = df_flex.groupby(col_dim)['arrecadado_sucesso'].sum().nlargest(5)
    top_arrecadacao_flex = _converter_para_df(df_flex, top_arrecadacao_flex, col_dim, 'total', total_flex)
    top_arrecadacao_sub = df_sub.groupby(col_dim)['arrecadado_sucesso'].sum().nlargest(5)
    top_arrecadacao_sub = _converter_para_df(df_sub, top_arrecadacao_sub, col_dim, 'total', total_sub)

    with open(f'{pasta_md}/{arquivo}.md', 'w', encoding='utf8') as md_descritivo:
        md_descritivo.write(f'{template.replace("$(nome_dimensao)", titulo)}')

        md_descritivo.write('\n')

        texto = _gerar_texto(ano, 'pontos-notaveis-total.template.md', mod_aon, titulo, top_campanhas_aon, col_dim, titulo_dim, 'total', 'Total')
        texto = texto.replace('$(top)', '5')
        md_descritivo.write(f'{texto}')
        texto = _gerar_texto(ano, 'pontos-notaveis-total.template.md', mod_flex, titulo, top_campanhas_flex, col_dim, titulo_dim, 'total', 'Total')
        texto = texto.replace('$(top)', '5')
        md_descritivo.write(f'{texto}')
        texto = _gerar_texto(ano, 'pontos-notaveis-total-recorrente.template.md', mod_sub, titulo, top_campanhas_sub, col_dim, titulo_dim, 'total', 'Total')
        texto = texto.replace('$(top)', '5')
        md_descritivo.write(f'{texto}')

        texto = _gerar_texto(ano, 'pontos-notaveis-taxa-sucesso.template.md', mod_aon, titulo, top_taxa_sucesso_aon, col_dim, titulo_dim, 'taxa_sucesso', 'Taxa de Sucesso')
        texto = texto.replace('$(top)', '5')
        md_descritivo.write(f'{texto}')
        texto = _gerar_texto(ano, 'pontos-notaveis-taxa-sucesso.template.md', mod_flex, titulo, top_taxa_sucesso_flex, col_dim, titulo_dim, 'taxa_sucesso', 'Taxa de Sucesso')
        texto = texto.replace('$(top)', '5')
        md_descritivo.write(f'{texto}')
        texto = _gerar_texto(ano, 'pontos-notaveis-taxa-sucesso-recorrente.template.md', mod_sub, titulo, top_taxa_sucesso_sub, col_dim, titulo_dim, 'taxa_sucesso', 'Taxa de Sucesso')
        texto = texto.replace('$(top)', '5')
        md_descritivo.write(f'{texto}')

        texto = _gerar_texto(ano, 'pontos-notaveis-valor-sucesso.template.md', mod_aon, titulo, top_arrecadacao_aon, col_dim, titulo_dim, 'arrecadado_sucesso', 'Arrecadado')
        texto = texto.replace('$(top)', '5')
        md_descritivo.write(f'{texto}')
        texto = _gerar_texto(ano, 'pontos-notaveis-valor-sucesso.template.md', mod_flex, titulo, top_arrecadacao_flex, col_dim, titulo_dim, 'arrecadado_sucesso', 'Arrecadado')
        texto = texto.replace('$(top)', '5')
        md_descritivo.write(f'{texto}')
        texto = _gerar_texto(ano, 'pontos-notaveis-valor-sucesso-recorrente.template.md', mod_sub, titulo, top_arrecadacao_sub, col_dim, titulo_dim, 'arrecadado_sucesso', 'Arrecadado')
        texto = texto.replace('$(top)', '5')
        md_descritivo.write(f'{texto}')        

        md_descritivo.close()

    return True


# gerar os rankings de campanhas por uf_br
def gerar_ranking_por_ufbr(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template):
    return gerar_ranking_por_coldim(df, ano, pasta_md, pasta_dados, arquivo, titulo, template, 'geral_uf_br', 'UF', 5, 5, 5)

# gerar os rankings de campanhas por gênero
def gerar_ranking_por_genero(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template):
    return gerar_ranking_por_coldim(df, ano, pasta_md, pasta_dados, arquivo, titulo, template, 'autoria_classificacao', 'Gênero', 5, 5, 5)

# gerar os rankings de campanhas por autoria
def gerar_ranking_por_autoria(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template):
    return gerar_ranking_por_coldim(df, ano, pasta_md, pasta_dados, arquivo, titulo, template, 'autoria_nome_publico', 'Autoria', 20, 20, 20)
