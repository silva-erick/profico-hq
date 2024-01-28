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
    texto = texto.replace('$(col_dim)', col_dim)

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

def _determinar_ranking_total(df, col_dim, ranking_total):
    # Crie uma cópia do DataFrame para evitar o aviso "SettingWithCopyWarning"
    df = df.copy()
    df['pontuacao_composta'] = 1000*df['total'] + df['taxa_sucesso']

    # Obter os índices dos maiores valores na pontuação composta
    top_indices_total = df.nlargest(ranking_total, 'pontuacao_composta').index

    # Filtrar o DataFrame original com base nos índices obtidos
    top_campanhas = df.loc[top_indices_total]

    #print(top_campanhas)

    return top_campanhas

# gerar os rankings de campanhas por col_dim
def gerar_ranking_por_coldim(df, ano, pasta_md, pasta_dados, arquivo, titulo, template, col_dim, titulo_dim, ranking_total, ranking_taxasucesso, ranking_valor, ranking_media, ranking_apoiomedio, ranking_contribuicoes):

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
    if ( ranking_total > 0):
        top_campanhas_aon = _determinar_ranking_total(df_aon, col_dim, ranking_total)
        top_campanhas_flex = df_flex.groupby(col_dim)['total'].mean().nlargest(ranking_total)
        top_campanhas_flex = _determinar_ranking_total(df_flex, col_dim, ranking_total)
        top_campanhas_sub = df_sub.groupby(col_dim)['total'].mean().nlargest(ranking_total)
        top_campanhas_sub = _determinar_ranking_total(df_sub, col_dim, ranking_total)

        comum.remover_colunas_apoio([
            top_campanhas_aon,
            top_campanhas_flex,
            top_campanhas_sub,
        ], [
            'pontuacao_composta',
        ])

    # Top 5 das UF com maiores taxas de sucesso para cada geral_modalidade
    if (ranking_contribuicoes > 0):
        top_contribuicoes_aon = df_aon.groupby(col_dim)['contribuicoes'].mean().nlargest(ranking_contribuicoes)
        top_contribuicoes_aon = _converter_para_df(df_aon, top_contribuicoes_aon, col_dim, 'total', total_aon)
        top_contribuicoes_flex = df_flex.groupby(col_dim)['contribuicoes'].mean().nlargest(ranking_contribuicoes)
        top_contribuicoes_flex = _converter_para_df(df_flex, top_contribuicoes_flex, col_dim, 'total', total_flex)
        top_contribuicoes_sub = df_sub.groupby(col_dim)['contribuicoes'].mean().nlargest(ranking_contribuicoes)
        top_contribuicoes_sub = _converter_para_df(df_sub, top_contribuicoes_sub, col_dim, 'total', total_sub)

        comum.remover_colunas_apoio([
            top_contribuicoes_aon,
            top_contribuicoes_flex,
            top_contribuicoes_sub,
        ], [
            'pontuacao_composta',
        ])

    # Top 5 das UF com maiores taxas de sucesso para cada geral_modalidade
    if (ranking_taxasucesso > 0):
        top_taxa_sucesso_aon = df_aon.groupby(col_dim)['taxa_sucesso'].mean().nlargest(ranking_taxasucesso)
        top_taxa_sucesso_aon = _converter_para_df(df_aon, top_taxa_sucesso_aon, col_dim, 'total', total_aon)
        top_taxa_sucesso_flex = df_flex.groupby(col_dim)['taxa_sucesso'].mean().nlargest(ranking_taxasucesso)
        top_taxa_sucesso_flex = _converter_para_df(df_flex, top_taxa_sucesso_flex, col_dim, 'total', total_flex)
        top_taxa_sucesso_sub = df_sub.groupby(col_dim)['taxa_sucesso'].mean().nlargest(ranking_taxasucesso)
        top_taxa_sucesso_sub = _converter_para_df(df_sub, top_taxa_sucesso_sub, col_dim, 'total', total_sub)

        comum.remover_colunas_apoio([
            top_taxa_sucesso_aon,
            top_taxa_sucesso_flex,
            top_taxa_sucesso_sub,
        ], [
            'pontuacao_composta',
        ])

    # Top 5 das UF com maior arrecadação para cada geral_modalidade
    if (ranking_valor > 0):
        top_arrecadacao_aon = df_aon.groupby(col_dim)['arrecadado_sucesso'].sum().nlargest(ranking_valor)
        top_arrecadacao_aon = _converter_para_df(df_aon, top_arrecadacao_aon, col_dim, 'total', total_aon)
        top_arrecadacao_flex = df_flex.groupby(col_dim)['arrecadado_sucesso'].sum().nlargest(ranking_valor)
        top_arrecadacao_flex = _converter_para_df(df_flex, top_arrecadacao_flex, col_dim, 'total', total_flex)
        top_arrecadacao_sub = df_sub.groupby(col_dim)['arrecadado_sucesso'].sum().nlargest(ranking_valor)
        top_arrecadacao_sub = _converter_para_df(df_sub, top_arrecadacao_sub, col_dim, 'total', total_sub)

        comum.remover_colunas_apoio([
            top_arrecadacao_aon,
            top_arrecadacao_flex,
            top_arrecadacao_sub,
        ], [
            'pontuacao_composta',
        ])

    # Top 5 das UF com maior arrecadação para cada geral_modalidade
    if (ranking_media > 0):
        top_media_aon = df_aon.groupby(col_dim)['media_sucesso'].sum().nlargest(ranking_valor)
        top_media_aon = _converter_para_df(df_aon, top_media_aon, col_dim, 'total', total_aon)
        top_media_flex = df_flex.groupby(col_dim)['media_sucesso'].sum().nlargest(ranking_valor)
        top_media_flex = _converter_para_df(df_flex, top_media_flex, col_dim, 'total', total_flex)
        top_media_sub = df_sub.groupby(col_dim)['media_sucesso'].sum().nlargest(ranking_valor)
        top_media_sub = _converter_para_df(df_sub, top_media_sub, col_dim, 'total', total_sub)

        comum.remover_colunas_apoio([
            top_media_aon,
            top_media_flex,
            top_media_sub,
        ], [
            'pontuacao_composta',
        ])

    # Top 5 das UF com maior arrecadação para cada geral_modalidade
    if (ranking_apoiomedio > 0):
        top_apoiomedio_aon = df_aon.groupby(col_dim)['apoio_medio'].sum().nlargest(ranking_valor)
        top_apoiomedio_aon = _converter_para_df(df_aon, top_apoiomedio_aon, col_dim, 'total', total_aon)
        top_apoiomedio_flex = df_flex.groupby(col_dim)['apoio_medio'].sum().nlargest(ranking_valor)
        top_apoiomedio_flex = _converter_para_df(df_flex, top_apoiomedio_flex, col_dim, 'total', total_flex)
        top_apoiomedio_sub = df_sub.groupby(col_dim)['apoio_medio'].sum().nlargest(ranking_valor)
        top_apoiomedio_sub = _converter_para_df(df_sub, top_apoiomedio_sub, col_dim, 'total', total_sub)

        comum.remover_colunas_apoio([
            top_apoiomedio_aon,
            top_apoiomedio_flex,
            top_apoiomedio_sub,
        ], [
            'pontuacao_composta',
        ])

    with open(f'{pasta_md}/{arquivo}.md', 'w', encoding='utf8') as md_descritivo:
        md_descritivo.write(f'{template.replace("$(nome_dimensao)", titulo)}')

        md_descritivo.write('\n')

        if ( ranking_total > 0):
            texto = _gerar_texto(ano, 'pontos-notaveis-total.template.md', mod_aon, titulo, top_campanhas_aon, col_dim, titulo_dim, 'total', 'Total')
            texto = texto.replace('$(top)', '5')
            md_descritivo.write(f'{texto}')
            texto = _gerar_texto(ano, 'pontos-notaveis-total.template.md', mod_flex, titulo, top_campanhas_flex, col_dim, titulo_dim, 'total', 'Total')
            texto = texto.replace('$(top)', '5')
            md_descritivo.write(f'{texto}')
            texto = _gerar_texto(ano, 'pontos-notaveis-total-recorrente.template.md', mod_sub, titulo, top_campanhas_sub, col_dim, titulo_dim, 'total', 'Total')
            texto = texto.replace('$(top)', '5')
            md_descritivo.write(f'{texto}')

        if ( ranking_contribuicoes > 0):
            texto = _gerar_texto(ano, 'pontos-notaveis-totalcontribuicoes.template.md', mod_aon, titulo, top_contribuicoes_aon, col_dim, titulo_dim, 'contribuicoes', 'Contribuições')
            texto = texto.replace('$(top)', '5')
            md_descritivo.write(f'{texto}')
            texto = _gerar_texto(ano, 'pontos-notaveis-totalcontribuicoes.template.md', mod_flex, titulo, top_contribuicoes_flex, col_dim, titulo_dim, 'contribuicoes', 'Contribuições')
            texto = texto.replace('$(top)', '5')
            md_descritivo.write(f'{texto}')
            texto = _gerar_texto(ano, 'pontos-notaveis-totalcontribuicoes-recorrente.template.md', mod_sub, titulo, top_contribuicoes_sub, col_dim, titulo_dim, 'contribuicoes', 'Contribuições')
            texto = texto.replace('$(top)', '5')
            md_descritivo.write(f'{texto}')

        if (ranking_taxasucesso > 0):
            texto = _gerar_texto(ano, 'pontos-notaveis-taxa-sucesso.template.md', mod_aon, titulo, top_taxa_sucesso_aon, col_dim, titulo_dim, 'taxa_sucesso', 'Taxa de Sucesso')
            texto = texto.replace('$(top)', '5')
            md_descritivo.write(f'{texto}')
            texto = _gerar_texto(ano, 'pontos-notaveis-taxa-sucesso.template.md', mod_flex, titulo, top_taxa_sucesso_flex, col_dim, titulo_dim, 'taxa_sucesso', 'Taxa de Sucesso')
            texto = texto.replace('$(top)', '5')
            md_descritivo.write(f'{texto}')
            texto = _gerar_texto(ano, 'pontos-notaveis-taxa-sucesso-recorrente.template.md', mod_sub, titulo, top_taxa_sucesso_sub, col_dim, titulo_dim, 'taxa_sucesso', 'Taxa de Sucesso')
            texto = texto.replace('$(top)', '5')
            md_descritivo.write(f'{texto}')

        if (ranking_valor > 0):
            texto = _gerar_texto(ano, 'pontos-notaveis-valor-sucesso.template.md', mod_aon, titulo, top_arrecadacao_aon, col_dim, titulo_dim, 'arrecadado_sucesso', 'Arrecadado')
            texto = texto.replace('$(top)', '5')
            md_descritivo.write(f'{texto}')
            texto = _gerar_texto(ano, 'pontos-notaveis-valor-sucesso.template.md', mod_flex, titulo, top_arrecadacao_flex, col_dim, titulo_dim, 'arrecadado_sucesso', 'Arrecadado')
            texto = texto.replace('$(top)', '5')
            md_descritivo.write(f'{texto}')
            texto = _gerar_texto(ano, 'pontos-notaveis-valor-sucesso-recorrente.template.md', mod_sub, titulo, top_arrecadacao_sub, col_dim, titulo_dim, 'arrecadado_sucesso', 'Arrecadado')
            texto = texto.replace('$(top)', '5')
            md_descritivo.write(f'{texto}')        

        if (ranking_media > 0):
            texto = _gerar_texto(ano, 'pontos-notaveis-media-sucesso.template.md', mod_aon, titulo, top_media_aon, col_dim, titulo_dim, 'media_sucesso', 'Arrecadação Média')
            texto = texto.replace('$(top)', '5')
            md_descritivo.write(f'{texto}')
            texto = _gerar_texto(ano, 'pontos-notaveis-media-sucesso.template.md', mod_flex, titulo, top_media_flex, col_dim, titulo_dim, 'media_sucesso', 'Arrecadação Média')
            texto = texto.replace('$(top)', '5')
            md_descritivo.write(f'{texto}')
            texto = _gerar_texto(ano, 'pontos-notaveis-media-sucesso-recorrente.template.md', mod_sub, titulo, top_media_sub, col_dim, titulo_dim, 'media_sucesso', 'Arrecadação Média')
            texto = texto.replace('$(top)', '5')
            md_descritivo.write(f'{texto}')        

        if (ranking_apoiomedio > 0):
            texto = _gerar_texto(ano, 'pontos-notaveis-mediaapoio-sucesso.template.md', mod_aon, titulo, top_apoiomedio_aon, col_dim, titulo_dim, 'apoio_medio', 'Apoio Médio')
            texto = texto.replace('$(top)', '5')
            md_descritivo.write(f'{texto}')
            texto = _gerar_texto(ano, 'pontos-notaveis-mediaapoio-sucesso.template.md', mod_flex, titulo, top_apoiomedio_flex, col_dim, titulo_dim, 'apoio_medio', 'Apoio Médio')
            texto = texto.replace('$(top)', '5')
            md_descritivo.write(f'{texto}')
            texto = _gerar_texto(ano, 'pontos-notaveis-mediaapoio-sucesso-recorrente.template.md', mod_sub, titulo, top_apoiomedio_sub, col_dim, titulo_dim, 'apoio_medio', 'Apoio Médio')
            texto = texto.replace('$(top)', '5')
            md_descritivo.write(f'{texto}')        

        md_descritivo.close()

    return True

# gerar os rankings de campanhas por uf_br
def gerar_ranking_por_ufbr(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template):
    return gerar_ranking_por_coldim(df, ano, pasta_md, pasta_dados, arquivo, titulo, template, 'geral_uf_br', 'UF', 5, 5, 5, 5, 5, 5)

# gerar os rankings de campanhas por gênero
def gerar_ranking_por_genero(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template):
    return gerar_ranking_por_coldim(df, ano, pasta_md, pasta_dados, arquivo, titulo, template, 'autoria_classificacao', 'Gênero', 5, 5, 5, 5, 5, 5)

# gerar os rankings de campanhas por autoria
def gerar_ranking_por_autoria(df, ano, pasta_md, pasta_dados, arquivo, titulo,  template):
    return gerar_ranking_por_coldim(df, ano, pasta_md, pasta_dados, arquivo, titulo, template, 'autoria_nome_publico', 'Autoria', 10, 0, 10, 10, 10, 10)
