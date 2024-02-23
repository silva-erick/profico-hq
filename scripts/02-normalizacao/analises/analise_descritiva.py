import analises.analise_lib as analisebase
import colunas as colunaslib
import pandas as pd
import os
import pydot


CAMINHO_CSV = "../../dados/csv"
CAMINHO_TEMPLATE = f"templates"
CAMINHO_TEMPLATE_DESCRITIVO = f"{CAMINHO_TEMPLATE}/descritivo"


class CoordenadorAnaliseDescritiva(analisebase.AnaliseInterface):

    """
    Coordenar a execução da análise descritiva
    """
    def executar(self, df, ano_referencia) -> bool:

        calc = CalculoIndicativos()
        print(f'> análise descritiva')
        print(f'\t. calcular indicadores: ', end='')
        resultado = calc.executar(df)
        print(f'{resultado}')

        if resultado:

            pasta_md = analisebase.garantir_pasta(f'{CAMINHO_CSV}/{ano_referencia}/analise_descritiva')
            pasta_dados = analisebase.garantir_pasta(f'{CAMINHO_CSV}/{ano_referencia}/analise_descritiva/dados')
            pasta_img = analisebase.garantir_pasta(f'{CAMINHO_CSV}/{ano_referencia}/analise_descritiva/img')

            resultado = (
                self._gerar_infografico(pasta_md, pasta_img, calc.df_resumo_mod, calc.df_resumo_mod_plataforma)
                and self._calcular_modalidades(calc, pasta_md, pasta_img, pasta_dados)
                and self._gerar_readme(calc, pasta_md)
            )

        return resultado

    """
    Gerar o infográfico
    """
    def _gerar_infografico(self, pasta_md, pasta_img, df_resumo, df_resumo_plataforma):

        resultado = True

        print('\t\t. gerar infográfico')

        with open(f'templates/descritivo/infografico.template.dot', 'r', encoding='utf8') as arq_template_dot_infografico:
            template_dot_infografico = arq_template_dot_infografico.read()
            arq_template_dot_infografico.close()

        with open(f'templates/descritivo/infografico.template.md', 'r', encoding='utf8') as arq_template_md_infografico:
            template_md_infografico = arq_template_md_infografico.read()
            arq_template_md_infografico.close()

        dot_geral = self._obter_template_infografico(template_dot_infografico, df_resumo)
        info_dot_geral = pydot.graph_from_dot_data(dot_geral)
        info_dot_geral[0].write_png(f'{pasta_img}/infografico-geral.png')

        dot_catarse = self._obter_template_infografico(template_dot_infografico, df_resumo_plataforma[
            df_resumo_plataforma[analisebase.DFCOL_ORIGEM] == analisebase.ORIGEM_CATARSE
        ])
        info_dot_catarse = pydot.graph_from_dot_data(dot_catarse)
        info_dot_catarse[0].write_png(f'{pasta_img}/infografico-catarse.png')

        dot_apoiase = self._obter_template_infografico(template_dot_infografico, df_resumo_plataforma[
            df_resumo_plataforma[analisebase.DFCOL_ORIGEM] == analisebase.ORIGEM_APOIASE
        ])
        info_dot_apoiase = pydot.graph_from_dot_data(dot_apoiase)
        info_dot_apoiase[0].write_png(f'{pasta_img}/infografico-apoiase.png')

        print('\t\t. gerar md dos infográficos')

        md_geral = self._obter_template_infografico(template_md_infografico, df_resumo)
        md_geral = md_geral.replace('$(tipo-infografico)', 'geral').replace('$(tipo-recorte)','Geral')
        with open(f'{pasta_md}/infografico-geral.md', 'w', encoding='utf8') as arq_md_infografico:
            arq_md_infografico.write(f'{md_geral}\n\n')

        md_catarse = self._obter_template_infografico(template_md_infografico, df_resumo_plataforma[
            df_resumo_plataforma[analisebase.DFCOL_ORIGEM] == analisebase.ORIGEM_CATARSE
        ])
        md_catarse = md_catarse.replace('$(tipo-infografico)', 'catarse').replace('$(tipo-recorte)','Catarse')
        with open(f'{pasta_md}/infografico-catarse.md', 'w', encoding='utf8') as arq_md_infografico:
            arq_md_infografico.write(f'{md_catarse}\n\n')

        md_apoiase = self._obter_template_infografico(template_md_infografico, df_resumo_plataforma[
            df_resumo_plataforma[analisebase.DFCOL_ORIGEM] == analisebase.ORIGEM_APOIASE
        ])
        md_apoiase = md_apoiase.replace('$(tipo-infografico)', 'apoiase').replace('$(tipo-recorte)','Apoia.se')
        with open(f'{pasta_md}/infografico-apoiase.md', 'w', encoding='utf8') as arq_md_infografico:
            arq_md_infografico.write(f'{md_apoiase}\n\n')

        return resultado

    """
    Obter o template de infográfico
    """
    def _obter_template_infografico(self, dot_template, df) -> str:

        lista_plataformas = []
        if analisebase.DFCOL_ORIGEM in df.columns:
            for orig in df[analisebase.DFCOL_ORIGEM].unique():
                lista_plataformas.append(analisebase.TITULOS_ORIGENS[orig])
        else:
            for orig in analisebase.ORIGENS:
                lista_plataformas.append(analisebase.TITULOS_ORIGENS[orig])


        df_pontuais = df[
            df[analisebase.DFCOL_MODALIDADE] != analisebase.CAMPANHA_SUB
        ]
        df_aon = df[
            df[analisebase.DFCOL_MODALIDADE] == analisebase.CAMPANHA_AON
        ]
        df_flex = df[
            df[analisebase.DFCOL_MODALIDADE] == analisebase.CAMPANHA_FLEX
        ]
        df_sub = df[
            df[analisebase.DFCOL_MODALIDADE] == analisebase.CAMPANHA_SUB
        ]

        valores_substituicao = {}
        valores_substituicao['$(plataformas)']                      = analisebase.enumerar_strings(lista_plataformas)
        valores_substituicao['$(menor-ano)']                        = df[df[analisebase.DFCOL_MENOR_ANO]!=0][analisebase.DFCOL_MENOR_ANO].min()
        valores_substituicao['$(maior-ano)']                        = df[analisebase.DFCOL_MAIOR_ANO].max()
        valores_substituicao['$(campanhas-total)']                  = analisebase.numero_com_separadores(df[analisebase.DFCOL_TOTAL].sum())
        valores_substituicao['$(campanhas-pontuais-total)']         = analisebase.numero_com_separadores(df_pontuais[analisebase.DFCOL_TOTAL].sum())

        valores_substituicao['$(campanhas-aon-total)']              = analisebase.numero_com_separadores(df_aon[analisebase.DFCOL_TOTAL].sum())
        valores_substituicao['$(campanhas-aon-sucesso)']            = analisebase.numero_com_separadores(100*df_aon[analisebase.DFCOL_TAXA_SUCESSO].sum(),1)
        valores_substituicao['$(campanhas-aon-total-arrecadado)']   = analisebase.numero_com_separadores(df_aon[analisebase.DFCOL_ARRECADADO_SUCESSO].sum(), 2)
        valores_substituicao['$(campanhas-aon-arrecadacao-media)']  = analisebase.numero_com_separadores(df_aon[analisebase.DFCOL_ARRECADADO_MED].sum(), 2)
        valores_substituicao['$(campanhas-aon-apoio-med)']          = analisebase.numero_com_separadores(df_aon[analisebase.DFCOL_APOIO_MED].sum(), 2)
        valores_substituicao['$(campanhas-aon-contr-totais)']       = analisebase.numero_com_separadores(df_aon[analisebase.DFCOL_CONTRIBUICOES].sum())
        valores_substituicao['$(campanhas-aon-contr-media)']        = analisebase.numero_com_separadores(df_aon[analisebase.DFCOL_CONTRIBUICOES_MED].sum())

        valores_substituicao['$(campanhas-flex-total)']             = analisebase.numero_com_separadores(df_flex[analisebase.DFCOL_TOTAL].sum())
        valores_substituicao['$(campanhas-flex-sucesso)']           = analisebase.numero_com_separadores(100*df_flex[analisebase.DFCOL_TAXA_SUCESSO].sum(),1)
        valores_substituicao['$(campanhas-flex-total-arrecadado)']  = analisebase.numero_com_separadores(df_flex[analisebase.DFCOL_ARRECADADO_SUCESSO].sum(), 2)
        valores_substituicao['$(campanhas-flex-arrecadacao-media)'] = analisebase.numero_com_separadores(df_flex[analisebase.DFCOL_ARRECADADO_MED].sum(), 2)
        valores_substituicao['$(campanhas-flex-apoio-med)']         = analisebase.numero_com_separadores(df_flex[analisebase.DFCOL_APOIO_MED].sum(), 2)
        valores_substituicao['$(campanhas-flex-contr-totais)']      = analisebase.numero_com_separadores(df_flex[analisebase.DFCOL_CONTRIBUICOES].sum())
        valores_substituicao['$(campanhas-flex-contr-media)']       = analisebase.numero_com_separadores(df_flex[analisebase.DFCOL_CONTRIBUICOES_MED].sum())

        valores_substituicao['$(campanhas-sub-total)']              = analisebase.numero_com_separadores(df_sub[analisebase.DFCOL_TOTAL].sum())
        valores_substituicao['$(campanhas-sub-sucesso)']            = analisebase.numero_com_separadores(100*df_sub[analisebase.DFCOL_TAXA_SUCESSO].sum(),1)
        valores_substituicao['$(campanhas-sub-total-arrecadado)']   = analisebase.numero_com_separadores(df_sub[analisebase.DFCOL_ARRECADADO_SUCESSO].sum(), 2)
        valores_substituicao['$(campanhas-sub-arrecadacao-media)']  = analisebase.numero_com_separadores(df_sub[analisebase.DFCOL_ARRECADADO_MED].sum(), 2)
        valores_substituicao['$(campanhas-sub-apoio-med)']          = analisebase.numero_com_separadores(df_sub[analisebase.DFCOL_APOIO_MED].sum(), 2)
        valores_substituicao['$(campanhas-sub-contr-totais)']       = analisebase.numero_com_separadores(df_sub[analisebase.DFCOL_CONTRIBUICOES].sum())
        valores_substituicao['$(campanhas-sub-contr-media)']        = analisebase.numero_com_separadores(df_sub[analisebase.DFCOL_CONTRIBUICOES_MED].sum())

        resultado = dot_template
        for k, v in valores_substituicao.items():
            if isinstance(v, str):
                valor = v
            else:
                valor = str(v)
            resultado = resultado.replace(k, valor)

        return resultado

    """
    Calcular modalidades
    """
    def _calcular_modalidades(self,calc, pasta_md, pasta_img, pasta_dados) -> bool:
        resultado = True
        
        print(f'\t. resumos:')
        print(f'\t\t. excel')
        resultado = self._gerar_excel_resumo(pasta_dados, calc.df_resumo_mod)
        print(f'\t\t. md')
        resultado = self._gerar_panorama_resumo(pasta_md, pasta_img, calc.df_resumo_mod)

        mapa_agrupamentos = {}
        mapa_agrupamentos['plataforma'] = {'chave': 'plataforma', 'nome': 'Plataforma', 'coluna': analisebase.DFCOL_ORIGEM}
        mapa_agrupamentos['genero'] = {'chave': 'genero', 'nome': 'Gênero', 'coluna': analisebase.DFCOL_GENERO}
        mapa_agrupamentos['uf'] = {'chave': 'uf', 'nome': 'UF', 'coluna': analisebase.DFCOL_UF}
        mapa_agrupamentos['mencoes'] = {'chave': 'mencoes', 'nome': 'Menções', 'coluna': analisebase.DFCOL_MENCAO}

        print(f'\t. cálculos das modalidades:')
        for mod in analisebase.MODALIDADES:
            print(f'\t\t. {mod}')

            df_resumo_mod_plataforma = calc.df_resumo_mod_plataforma[
                calc.df_resumo_mod_plataforma[analisebase.DFCOL_MODALIDADE] == mod
            ]
            df_resumo_mod_genero = calc.df_resumo_mod_genero[
                calc.df_resumo_mod_genero[analisebase.DFCOL_MODALIDADE] == mod
            ]
            df_resumo_mod_uf = calc.df_resumo_mod_uf[
                calc.df_resumo_mod_uf[analisebase.DFCOL_MODALIDADE] == mod
            ]
            df_resumo_mod_mencoes = calc.df_resumo_mod_mencoes[
                calc.df_resumo_mod_mencoes[analisebase.DFCOL_MODALIDADE] == mod
            ]

            print(f'\t\t\t. gerar md plataforma')
            resultado = self._gerar_md_recorte(mod, pasta_md, pasta_img, df_resumo_mod_plataforma, mapa_agrupamentos['plataforma'])
            print(f'\t\t\t. gerar md gênero')
            resultado = self._gerar_md_recorte(mod, pasta_md, pasta_img, df_resumo_mod_genero, mapa_agrupamentos['genero'])
            print(f'\t\t\t. gerar md UF')
            resultado = self._gerar_md_recorte(mod, pasta_md, pasta_img, df_resumo_mod_uf, mapa_agrupamentos['uf'])
            print(f'\t\t\t. gerar md menções')
            resultado = self._gerar_md_recorte(mod, pasta_md, pasta_img, df_resumo_mod_mencoes, mapa_agrupamentos['mencoes'])

            print(f'\t\t\t. gerar excel')
            resultado = self._gerar_excel(pasta_dados, mod,
                            df_resumo_mod_plataforma,
                            df_resumo_mod_genero,
                            df_resumo_mod_uf,
                            df_resumo_mod_mencoes
                            )
            
        return resultado
    
    """
    Gerar markdown do recorte a partir de um template
    """
    def _gerar_md_recorte(self, mod, pasta_md, pasta_img, df_recorte, mapa_agrupamento):

        recorte = mapa_agrupamento['chave']
        coluna = mapa_agrupamento['coluna']
        titulo = mapa_agrupamento['nome']

        resultado = True

        with open(f'templates/descritivo/recorte.template.md', 'r', encoding='utf8') as arq_template:
            template_recorte = arq_template.read()

        template_recorte = template_recorte.replace('$(tabela-markdown)', self._obter_tabela_markdown_resumo(df_recorte)).replace('$(mod)',mod).replace('$(recorte)', recorte).replace('$(titulo-recorte)', titulo)
        
        with open(f'{pasta_md}/{mod}-{recorte}.md', 'w', encoding='utf8') as arq_recorte:
            arq_recorte.write(f'{template_recorte}\n')

        analisebase._gerar_grafico_barras_horizontais2y(
            pasta_img,
            f'{mod}-{recorte}-totais',
            df_recorte,
            coluna,
            analisebase.DFCOL_TOTAL,
            analisebase.DFCOL_TOTAL_SUCESSO,
            f'Totais (Modalidade: {analisebase.TITULOS_MODALIDADES[mod]} e {titulo})',
            titulo,
            'Campanhas',
            'Campanhas',
            'Campanhas Bem Sucedidas',
            analisebase.numero_inteiro_f
            )

        analisebase._gerar_grafico_barras_horizontais(
            pasta_img,
            f'{mod}-{recorte}-participacao',
            df_recorte,
            coluna,
            analisebase.DFCOL_PARTICIP,
            f'Participação (Modalidade: {analisebase.TITULOS_MODALIDADES[mod]} e {titulo})',
            titulo,
            'Participação',
            'Participação',
            analisebase.numero_percent1_f,
            analisebase.formatar_percent_eixo_y
            )

        analisebase._gerar_grafico_barras_horizontais(
            pasta_img,
            f'{mod}-{recorte}-taxa-sucesso',
            df_recorte,
            coluna,
            analisebase.DFCOL_TAXA_SUCESSO,
            f'Taxa de Sucesso (Modalidade: {analisebase.TITULOS_MODALIDADES[mod]} e {titulo})',
            titulo,
            'Taxa de Sucesso',
            'Taxa de Sucesso',
            analisebase.numero_percent1_f,
            analisebase.formatar_percent_eixo_y
            )

        analisebase._gerar_grafico_barras_horizontais(
            pasta_img,
            f'{mod}-{recorte}-meta',
            df_recorte,
            coluna,
            analisebase.DFCOL_META,
            f'Meta Total (Modalidade: {analisebase.TITULOS_MODALIDADES[mod]} e {titulo})',
            titulo,
            'Meta Total (R$)',
            'Meta Total (R$)',
            analisebase.numero_real2_f
            )

        analisebase._gerar_grafico_barras_horizontais(
            pasta_img,
            f'{mod}-{recorte}-meta-med',
            df_recorte,
            coluna,
            analisebase.DFCOL_META_MED,
            f'Meta Média (Modalidade: {analisebase.TITULOS_MODALIDADES[mod]} e {titulo})',
            titulo,
            'Meta Média (R$)',
            'Meta Média (R$)',
            analisebase.numero_real2_f
            )

        analisebase._gerar_grafico_barras_horizontais(
            pasta_img,
            f'{mod}-{recorte}-total-arrecadado',
            df_recorte,
            coluna,
            analisebase.DFCOL_ARRECADADO_SUCESSO,
            f'Total Arrecadado (Modalidade: {analisebase.TITULOS_MODALIDADES[mod]} e {titulo})',
            titulo,
            'Total Arrecadado (R$)',
            'Total Arrecadado (R$)',
            analisebase.numero_real2_f
            )

        analisebase._gerar_grafico_barras_horizontais(
            pasta_img,
            f'{mod}-{recorte}-media-arrecadada',
            df_recorte,
            coluna,
            analisebase.DFCOL_ARRECADADO_MED,
            f'Média Arrecadada por Campanha (Modalidade: {analisebase.TITULOS_MODALIDADES[mod]} e {titulo})',
            titulo,
            'Média Arrecadada por Campanha (R$)',
            'Média Arrecadada por Campanha (R$)',
            analisebase.numero_real2_f
            )

        analisebase._gerar_grafico_barras_horizontais(
            pasta_img,
            f'{mod}-{recorte}-apoio-medio',
            df_recorte,
            coluna,
            analisebase.DFCOL_APOIO_MED,
            f'Apoio Médio por Campanha (Modalidade: {analisebase.TITULOS_MODALIDADES[mod]} e {titulo})',
            titulo,
            'Apoio Médio por Campanha (R$)',
            'Apoio Médio por Campanha (R$)',
            analisebase.numero_real2_f
            )

        analisebase._gerar_grafico_barras_horizontais(
            pasta_img,
            f'{mod}-{recorte}-total-contribuicoes',
            df_recorte,
            coluna,
            analisebase.DFCOL_CONTRIBUICOES,
            f'Total de Contribuições (Modalidade: {analisebase.TITULOS_MODALIDADES[mod]} e {titulo})',
            titulo,
            'Total de Contribuições',
            'Total de Contribuições',
            analisebase.numero_inteiro_f
            )

        analisebase._gerar_grafico_barras_horizontais(
            pasta_img,
            f'{mod}-{recorte}-media-contribuicoes',
            df_recorte,
            coluna,
            analisebase.DFCOL_CONTRIBUICOES_MED,
            f'Média de Contribuições por Campanha (Modalidade: {analisebase.TITULOS_MODALIDADES[mod]} e {titulo})',
            titulo,
            'Média de Contribuições por Campanha',
            'Média de Contribuições por Campanha',
            analisebase.numero_real1_f
            )
        
        return resultado

    """
    Obter tabela markdown resumo
    """
    def _obter_tabela_markdown_resumo(self, df_resumo):
        
        df_formatado = df_resumo.copy()

        df_formatado = df_formatado.drop(analisebase.DFCOL_MENOR_ANO, axis=1)
        df_formatado = df_formatado.drop(analisebase.DFCOL_MAIOR_ANO, axis=1)

        df_formatado[analisebase.DFCOL_TOTAL]                   = df_formatado[analisebase.DFCOL_TOTAL].map(analisebase.numero_inteiro_f)
        df_formatado[analisebase.DFCOL_TOTAL_SUCESSO]           = df_formatado[analisebase.DFCOL_TOTAL_SUCESSO].map(analisebase.numero_inteiro_f)
        df_formatado[analisebase.DFCOL_PARTICIP]                = df_formatado[analisebase.DFCOL_PARTICIP].map(analisebase.numero_percent1_f)
        df_formatado[analisebase.DFCOL_TAXA_SUCESSO]            = df_formatado[analisebase.DFCOL_TAXA_SUCESSO].map(analisebase.numero_percent1_f)

        df_formatado[analisebase.DFCOL_META]                    = df_formatado[analisebase.DFCOL_META].map(analisebase.numero_real2_f)
        df_formatado[analisebase.DFCOL_META_MED]                = df_formatado[analisebase.DFCOL_META_MED].map(analisebase.numero_real2_f)
        df_formatado[analisebase.DFCOL_META_STD]                = df_formatado[analisebase.DFCOL_META_STD].map(analisebase.numero_real2_f)
        df_formatado[analisebase.DFCOL_META_MIN]                = df_formatado[analisebase.DFCOL_META_MIN].map(analisebase.numero_real2_f)
        df_formatado[analisebase.DFCOL_META_MAX]                = df_formatado[analisebase.DFCOL_META_MAX].map(analisebase.numero_real2_f)

        df_formatado[analisebase.DFCOL_ARRECADADO_SUCESSO]      = df_formatado[analisebase.DFCOL_ARRECADADO_SUCESSO].map(analisebase.numero_real2_f)
        df_formatado[analisebase.DFCOL_ARRECADADO_MED]          = df_formatado[analisebase.DFCOL_ARRECADADO_MED].map(analisebase.numero_real2_f)
        df_formatado[analisebase.DFCOL_ARRECADADO_STD]          = df_formatado[analisebase.DFCOL_ARRECADADO_STD].map(analisebase.numero_real2_f)
        df_formatado[analisebase.DFCOL_ARRECADADO_MIN]          = df_formatado[analisebase.DFCOL_ARRECADADO_MIN].map(analisebase.numero_real2_f)
        df_formatado[analisebase.DFCOL_ARRECADADO_MAX]          = df_formatado[analisebase.DFCOL_ARRECADADO_MAX].map(analisebase.numero_real2_f)
        df_formatado[analisebase.DFCOL_APOIO_MED]               = df_formatado[analisebase.DFCOL_APOIO_MED].map(analisebase.numero_real2_f)
        df_formatado[analisebase.DFCOL_APOIO_STD]               = df_formatado[analisebase.DFCOL_APOIO_STD].map(analisebase.numero_real2_f)
        df_formatado[analisebase.DFCOL_APOIO_MIN]               = df_formatado[analisebase.DFCOL_APOIO_MIN].map(analisebase.numero_real2_f)
        df_formatado[analisebase.DFCOL_APOIO_MAX]               = df_formatado[analisebase.DFCOL_APOIO_MAX].map(analisebase.numero_real2_f)
        df_formatado[analisebase.DFCOL_CONTRIBUICOES]           = df_formatado[analisebase.DFCOL_CONTRIBUICOES].map(analisebase.numero_inteiro_f)
        df_formatado[analisebase.DFCOL_CONTRIBUICOES_MED]       = df_formatado[analisebase.DFCOL_CONTRIBUICOES_MED].map(analisebase.numero_real1_f)
        df_formatado[analisebase.DFCOL_CONTRIBUICOES_STD]       = df_formatado[analisebase.DFCOL_CONTRIBUICOES_STD].map(analisebase.numero_real1_f)
        df_formatado[analisebase.DFCOL_CONTRIBUICOES_MIN]       = df_formatado[analisebase.DFCOL_CONTRIBUICOES_MIN].map(analisebase.numero_real1_f)
        df_formatado[analisebase.DFCOL_CONTRIBUICOES_MAX]       = df_formatado[analisebase.DFCOL_CONTRIBUICOES_MAX].map(analisebase.numero_real1_f)

        alinhamento_md = []
        for c in df_resumo.columns:
            if c == analisebase.DFCOL_MENOR_ANO:
                continue
            if c == analisebase.DFCOL_MAIOR_ANO:
                continue
            
            d = df_resumo[c].dtype.name
            if d == 'int64':
                alinhamento_md.append('right')
            elif d == 'float64':
                alinhamento_md.append('right')
            else:
                alinhamento_md.append('left')

        df_formatado.rename(columns={analisebase.DFCOL_PARTICIP: f'{analisebase.DFCOL_PARTICIP} (%)' }, inplace=True)
        df_formatado.rename(columns={analisebase.DFCOL_TAXA_SUCESSO: f'{analisebase.DFCOL_TAXA_SUCESSO} (%)' }, inplace=True)
        df_formatado.rename(columns={analisebase.DFCOL_META: f'{analisebase.DFCOL_META} (R$)' }, inplace=True)
        df_formatado.rename(columns={analisebase.DFCOL_META_MED: f'{analisebase.DFCOL_META_MED} (R$)' }, inplace=True)
        df_formatado.rename(columns={analisebase.DFCOL_META_STD: f'{analisebase.DFCOL_META_STD} (R$)' }, inplace=True)
        df_formatado.rename(columns={analisebase.DFCOL_META_MIN: f'{analisebase.DFCOL_META_MIN} (R$)' }, inplace=True)
        df_formatado.rename(columns={analisebase.DFCOL_META_MAX: f'{analisebase.DFCOL_META_MAX} (R$)' }, inplace=True)
        df_formatado.rename(columns={analisebase.DFCOL_ARRECADADO_SUCESSO: f'{analisebase.DFCOL_ARRECADADO_SUCESSO} (R$)' }, inplace=True)
        df_formatado.rename(columns={analisebase.DFCOL_ARRECADADO_MED: f'{analisebase.DFCOL_ARRECADADO_MED} (R$)' }, inplace=True)
        df_formatado.rename(columns={analisebase.DFCOL_ARRECADADO_STD: f'{analisebase.DFCOL_ARRECADADO_STD} (R$)' }, inplace=True)
        df_formatado.rename(columns={analisebase.DFCOL_ARRECADADO_MIN: f'{analisebase.DFCOL_ARRECADADO_MIN} (R$)' }, inplace=True)
        df_formatado.rename(columns={analisebase.DFCOL_ARRECADADO_MAX: f'{analisebase.DFCOL_ARRECADADO_MAX} (R$)' }, inplace=True)
        df_formatado.rename(columns={analisebase.DFCOL_APOIO_MED: f'{analisebase.DFCOL_APOIO_MED} (R$)' }, inplace=True)
        df_formatado.rename(columns={analisebase.DFCOL_APOIO_STD: f'{analisebase.DFCOL_APOIO_STD} (R$)' }, inplace=True)
        df_formatado.rename(columns={analisebase.DFCOL_APOIO_MIN: f'{analisebase.DFCOL_APOIO_MIN} (R$)' }, inplace=True)
        df_formatado.rename(columns={analisebase.DFCOL_APOIO_MAX: f'{analisebase.DFCOL_APOIO_MAX} (R$)' }, inplace=True)
        df_formatado.rename(columns={analisebase.DFCOL_CONTRIBUICOES: f'{analisebase.DFCOL_CONTRIBUICOES}' }, inplace=True)
        df_formatado.rename(columns={analisebase.DFCOL_CONTRIBUICOES_MED: f'{analisebase.DFCOL_CONTRIBUICOES_MED}' }, inplace=True)
        df_formatado.rename(columns={analisebase.DFCOL_CONTRIBUICOES_STD: f'{analisebase.DFCOL_CONTRIBUICOES_STD}' }, inplace=True)
        df_formatado.rename(columns={analisebase.DFCOL_CONTRIBUICOES_MIN: f'{analisebase.DFCOL_CONTRIBUICOES_MIN}' }, inplace=True)
        df_formatado.rename(columns={analisebase.DFCOL_CONTRIBUICOES_MAX: f'{analisebase.DFCOL_CONTRIBUICOES_MAX}' }, inplace=True)

        resultado = df_formatado.to_markdown(index=False, disable_numparse=True, colalign=alinhamento_md)

        return resultado

    """
    Gerar panorama.md a partir de template
    """
    def _gerar_panorama_resumo(self, pasta_md, pasta_img, df_resumo):

        resultado = True

        with open(f'templates/descritivo/panorama.template.md', 'r', encoding='utf8') as arq_template:
            template_panorama = arq_template.read()

        template_panorama = template_panorama.replace('$(tabela-markdown)', self._obter_tabela_markdown_resumo(df_resumo))
        
        with open(f'{pasta_md}/panorama.md', 'w', encoding='utf8') as arq_panorama:
            arq_panorama.write(f'{template_panorama}\n')

        analisebase._gerar_grafico_barras_horizontais2y(
            pasta_img,
            'panorama-totais',
            df_resumo,
            analisebase.DFCOL_MODALIDADE,
            analisebase.DFCOL_TOTAL,
            analisebase.DFCOL_TOTAL_SUCESSO,
            'Totais (Modalidade)',
            'Modalidade',
            'Campanhas',
            'Campanhas',
            'Campanhas Bem Sucedidas',
            analisebase.numero_inteiro_f
            )

        analisebase._gerar_grafico_barras_horizontais(
            pasta_img,
            'panorama-participacao',
            df_resumo,
            analisebase.DFCOL_MODALIDADE,
            analisebase.DFCOL_PARTICIP,
            'Participação (Modalidade)',
            'Modalidade',
            'Participação',
            'Participação',
            analisebase.numero_percent1_f,
            analisebase.formatar_percent_eixo_y
            )

        analisebase._gerar_grafico_barras_horizontais(
            pasta_img,
            'panorama-taxa-sucesso',
            df_resumo,
            analisebase.DFCOL_MODALIDADE,
            analisebase.DFCOL_TAXA_SUCESSO,
            'Taxa de Sucesso (Modalidade)',
            'Modalidade',
            'Taxa de Sucesso',
            'Taxa de Sucesso',
            analisebase.numero_percent1_f,
            analisebase.formatar_percent_eixo_y
            )

        analisebase._gerar_grafico_barras_horizontais(
            pasta_img,
            'panorama-meta',
            df_resumo,
            analisebase.DFCOL_MODALIDADE,
            analisebase.DFCOL_META,
            'Meta Total (Modalidade)',
            'Modalidade',
            'Meta Total (R$)',
            'Meta Total (R$)',
            analisebase.numero_real2_f
            )

        analisebase._gerar_grafico_barras_horizontais(
            pasta_img,
            'panorama-meta-med',
            df_resumo,
            analisebase.DFCOL_MODALIDADE,
            analisebase.DFCOL_META_MED,
            'Meta Média (Modalidade)',
            'Modalidade',
            'Meta Média (R$)',
            'Meta Média (R$)',
            analisebase.numero_real2_f
            )

        analisebase._gerar_grafico_barras_horizontais(
            pasta_img,
            'panorama-total-arrecadado',
            df_resumo,
            analisebase.DFCOL_MODALIDADE,
            analisebase.DFCOL_ARRECADADO_SUCESSO,
            'Total Arrecadado (Modalidade)',
            'Modalidade',
            'Total Arrecadado (R$)',
            'Total Arrecadado (R$)',
            analisebase.numero_real2_f
            )

        analisebase._gerar_grafico_barras_horizontais(
            pasta_img,
            'panorama-media-arrecadada',
            df_resumo,
            analisebase.DFCOL_MODALIDADE,
            analisebase.DFCOL_ARRECADADO_MED,
            'Média Arrecadada por Campanha (Modalidade)',
            'Modalidade',
            'Média Arrecadada por Campanha (R$)',
            'Média Arrecadada por Campanha (R$)',
            analisebase.numero_real2_f
            )

        analisebase._gerar_grafico_barras_horizontais(
            pasta_img,
            'panorama-apoio-medio',
            df_resumo,
            analisebase.DFCOL_MODALIDADE,
            analisebase.DFCOL_APOIO_MED,
            'Apoio Médio por Campanha (Modalidade)',
            'Modalidade',
            'Apoio Médio por Campanha (R$)',
            'Apoio Médio por Campanha (R$)',
            analisebase.numero_real2_f
            )

        analisebase._gerar_grafico_barras_horizontais(
            pasta_img,
            'panorama-total-contribuicoes',
            df_resumo,
            analisebase.DFCOL_MODALIDADE,
            analisebase.DFCOL_CONTRIBUICOES,
            'Total de Contribuições (Modalidade)',
            'Modalidade',
            'Total de Contribuições',
            'Total de Contribuições',
            analisebase.numero_inteiro_f
            )

        analisebase._gerar_grafico_barras_horizontais(
            pasta_img,
            'panorama-media-contribuicoes',
            df_resumo,
            analisebase.DFCOL_MODALIDADE,
            analisebase.DFCOL_CONTRIBUICOES_MED,
            'Média de Contribuições por Campanha (Modalidade)',
            'Modalidade',
            'Média de Contribuições por Campanha',
            'Média de Contribuições por Campanha',
            analisebase.numero_real1_f
            )
        
        return resultado

    """
    Gerar o excel da modalidade informada
    """
    def _gerar_excel_resumo(self, pasta_dados, df_resumo):

        resultado = True

        formatados = {}
        formatados[analisebase.DFCOL_TOTAL] = {'num_format': '#,##0'}
        formatados[analisebase.DFCOL_TOTAL_SUCESSO] = {'num_format': '#,##0'}
        formatados[analisebase.DFCOL_PARTICIP] = {'num_format': '0.00%'}
        formatados[analisebase.DFCOL_PARTICIP] = {'num_format': '0.00%'}
        formatados[analisebase.DFCOL_TAXA_SUCESSO] = {'num_format': '0.00%'}
        formatados[analisebase.DFCOL_META] = {'num_format': 'R$ #,##0.00'}
        formatados[analisebase.DFCOL_META_MED] = {'num_format': 'R$ #,##0.00'}
        formatados[analisebase.DFCOL_META_STD] = {'num_format': 'R$ #,##0.00'}
        formatados[analisebase.DFCOL_META_MIN] = {'num_format': 'R$ #,##0.00'}
        formatados[analisebase.DFCOL_META_MAX] = {'num_format': 'R$ #,##0.00'}
        formatados[analisebase.DFCOL_ARRECADADO_SUCESSO] = {'num_format': 'R$ #,##0.00'}
        formatados[analisebase.DFCOL_ARRECADADO_MED] = {'num_format': 'R$ #,##0.00'}
        formatados[analisebase.DFCOL_ARRECADADO_STD] = {'num_format': 'R$ #,##0.00'}
        formatados[analisebase.DFCOL_ARRECADADO_MIN] = {'num_format': 'R$ #,##0.00'}
        formatados[analisebase.DFCOL_ARRECADADO_MAX] = {'num_format': 'R$ #,##0.00'}
        formatados[analisebase.DFCOL_APOIO_MED] = {'num_format': 'R$ #,##0.00'}
        formatados[analisebase.DFCOL_APOIO_STD] = {'num_format': 'R$ #,##0.00'}
        formatados[analisebase.DFCOL_APOIO_MIN] = {'num_format': 'R$ #,##0.00'}
        formatados[analisebase.DFCOL_APOIO_MAX] = {'num_format': 'R$ #,##0.00'}
        formatados[analisebase.DFCOL_CONTRIBUICOES] = {'num_format': '#,##0'}
        formatados[analisebase.DFCOL_CONTRIBUICOES_MED] = {'num_format': '#,##0'}
        formatados[analisebase.DFCOL_CONTRIBUICOES_STD] = {'num_format': '#,##0'}
        formatados[analisebase.DFCOL_CONTRIBUICOES_MIN] = {'num_format': '#,##0'}
        formatados[analisebase.DFCOL_CONTRIBUICOES_MAX] = {'num_format': '#,##0'}
        
        analisebase.GeracaoExcel.executar(df_resumo, f'{pasta_dados}/panorama.xlsx', formatados)
        
        return resultado

    """
    Gerar o excel da modalidade informada
    """
    def _gerar_excel(self, pasta_dados, mod, df_resumo_mod_plataforma, df_resumo_mod_genero, df_resumo_mod_uf, df_resumo_mod_mencoes):

        resultado = True

        formatados = {}
        formatados[analisebase.DFCOL_TOTAL] = {'num_format': '#,##0'}
        formatados[analisebase.DFCOL_TOTAL_SUCESSO] = {'num_format': '#,##0'}
        formatados[analisebase.DFCOL_PARTICIP] = {'num_format': '0.00%'}
        formatados[analisebase.DFCOL_PARTICIP] = {'num_format': '0.00%'}
        formatados[analisebase.DFCOL_TAXA_SUCESSO] = {'num_format': '0.00%'}
        formatados[analisebase.DFCOL_META] = {'num_format': 'R$ #,##0.00'}
        formatados[analisebase.DFCOL_META_MED] = {'num_format': 'R$ #,##0.00'}
        formatados[analisebase.DFCOL_META_STD] = {'num_format': 'R$ #,##0.00'}
        formatados[analisebase.DFCOL_META_MIN] = {'num_format': 'R$ #,##0.00'}
        formatados[analisebase.DFCOL_META_MAX] = {'num_format': 'R$ #,##0.00'}
        formatados[analisebase.DFCOL_ARRECADADO_SUCESSO] = {'num_format': 'R$ #,##0.00'}
        formatados[analisebase.DFCOL_ARRECADADO_MED] = {'num_format': 'R$ #,##0.00'}
        formatados[analisebase.DFCOL_ARRECADADO_STD] = {'num_format': 'R$ #,##0.00'}
        formatados[analisebase.DFCOL_ARRECADADO_MIN] = {'num_format': 'R$ #,##0.00'}
        formatados[analisebase.DFCOL_ARRECADADO_MAX] = {'num_format': 'R$ #,##0.00'}
        formatados[analisebase.DFCOL_APOIO_MED] = {'num_format': 'R$ #,##0.00'}
        formatados[analisebase.DFCOL_APOIO_STD] = {'num_format': 'R$ #,##0.00'}
        formatados[analisebase.DFCOL_APOIO_MIN] = {'num_format': 'R$ #,##0.00'}
        formatados[analisebase.DFCOL_APOIO_MAX] = {'num_format': 'R$ #,##0.00'}
        formatados[analisebase.DFCOL_CONTRIBUICOES] = {'num_format': '#,##0'}
        formatados[analisebase.DFCOL_CONTRIBUICOES_MED] = {'num_format': '#,##0'}
        formatados[analisebase.DFCOL_CONTRIBUICOES_STD] = {'num_format': '#,##0'}
        formatados[analisebase.DFCOL_CONTRIBUICOES_MIN] = {'num_format': '#,##0'}
        formatados[analisebase.DFCOL_CONTRIBUICOES_MAX] = {'num_format': '#,##0'}
        
        analisebase.GeracaoExcel.executar(df_resumo_mod_plataforma, f'{pasta_dados}/{mod}-plataforma.xlsx', formatados)
        analisebase.GeracaoExcel.executar(df_resumo_mod_genero, f'{pasta_dados}/{mod}-genero.xlsx', formatados)
        analisebase.GeracaoExcel.executar(df_resumo_mod_uf, f'{pasta_dados}/{mod}-uf.xlsx', formatados)
        analisebase.GeracaoExcel.executar(df_resumo_mod_mencoes, f'{pasta_dados}/{mod}-mencoes.xlsx', formatados)
        
        return resultado

    """
    Gerar arquivo README.md a partir de template
    """
    def _gerar_readme(self, calc, pasta_md) -> bool:
        resultado = True

        with open(f'templates/descritivo/README.template.md', 'r', encoding='utf8') as arq_template:
            template_readme = arq_template.read()

        with open(f'{pasta_md}/README.md', 'w', encoding='utf8') as arq_readme:
            arq_readme.write(template_readme)
            # modalidades = calc.df_resumo_mod[analisebase.DFCOL_MODALIDADE].unique()
            # for mod in modalidades:
            #     arq_readme.write(f'## {analisebase.TITULOS_MODALIDADES[mod]}\n\n')
            #     arq_readme.write('lero lero\n\n')

        return resultado


class CalculoIndicativos(analisebase.AnaliseInterface):

    """
    Executar a análise descritiva agrupando 
    """
    def executar(self, df_completo) -> bool:

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
        if modalidade == analisebase.CAMPANHA_SUB:
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
        df_resumo = df_completo.groupby(colunas).size().reset_index(name=analisebase.DFCOL_TOTAL)

        total = df_resumo[analisebase.DFCOL_TOTAL].sum()

        # estender o df com mais colunas
        for index, row in df_resumo.iterrows():
            modalidade = row[colunaslib.COL_GERAL_MODALIDADE]
            total_mod = row[analisebase.DFCOL_TOTAL]

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
            
            df_resumo.at[index, analisebase.DFCOL_TOTAL]                = int(total_mod)
            df_resumo.at[index, analisebase.DFCOL_TOTAL_SUCESSO]        = int(total_mod_sucesso)
            df_resumo.at[index, analisebase.DFCOL_PARTICIP]             = analisebase._dividir(total_mod, total)
            df_resumo.at[index, analisebase.DFCOL_TAXA_SUCESSO]         = analisebase._dividir(total_mod_sucesso, total_mod)
            df_resumo.at[index, analisebase.DFCOL_META]                 = meta_mod_sucesso
            df_resumo.at[index, analisebase.DFCOL_META_MED]             = meta_mod_sucesso_med
            df_resumo.at[index, analisebase.DFCOL_META_STD]             = meta_mod_sucesso_std
            df_resumo.at[index, analisebase.DFCOL_META_MIN]             = meta_mod_sucesso_min
            df_resumo.at[index, analisebase.DFCOL_META_MAX]             = meta_mod_sucesso_max
            df_resumo.at[index, analisebase.DFCOL_ARRECADADO_SUCESSO]   = valor_mod_sucesso
            df_resumo.at[index, analisebase.DFCOL_ARRECADADO_MED]       = valor_med_mod_sucesso
            df_resumo.at[index, analisebase.DFCOL_ARRECADADO_STD]       = valor_std_mod_sucesso
            df_resumo.at[index, analisebase.DFCOL_ARRECADADO_MIN]       = valor_min_mod_sucesso
            df_resumo.at[index, analisebase.DFCOL_ARRECADADO_MAX]       = valor_max_mod_sucesso
            df_resumo.at[index, analisebase.DFCOL_APOIO_MED]            = apoio_med_mod_sucesso
            df_resumo.at[index, analisebase.DFCOL_APOIO_STD]            = apoio_std_mod_sucesso
            df_resumo.at[index, analisebase.DFCOL_APOIO_MIN]            = apoio_min_mod_sucesso
            df_resumo.at[index, analisebase.DFCOL_APOIO_MAX]            = apoio_max_mod_sucesso
            df_resumo.at[index, analisebase.DFCOL_CONTRIBUICOES]        = contribuicoes
            df_resumo.at[index, analisebase.DFCOL_CONTRIBUICOES_MED]    = contribuicoes_med
            df_resumo.at[index, analisebase.DFCOL_CONTRIBUICOES_STD]    = contribuicoes_std
            df_resumo.at[index, analisebase.DFCOL_CONTRIBUICOES_MIN]    = contribuicoes_min
            df_resumo.at[index, analisebase.DFCOL_CONTRIBUICOES_MAX]    = contribuicoes_max
            df_resumo.at[index, analisebase.DFCOL_MENOR_ANO]            = menor_ano
            df_resumo.at[index, analisebase.DFCOL_MAIOR_ANO]            = maior_ano


        # Preencher NaN com 0 para evitar problemas na divisão
        df_resumo = df_resumo.fillna(0)
        df_resumo.rename(columns={colunaslib.COL_GERAL_MODALIDADE: analisebase.DFCOL_MODALIDADE}, inplace=True)

        df_resumo[analisebase.DFCOL_MENOR_ANO]       = df_resumo[analisebase.DFCOL_MENOR_ANO].round().astype('int64')
        df_resumo[analisebase.DFCOL_MAIOR_ANO]       = df_resumo[analisebase.DFCOL_MAIOR_ANO].round().astype('int64')


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

            df_resultado.at[index, analisebase.DFCOL_TOTAL]                 = int(total_recorte_mod)
            df_resultado.at[index, analisebase.DFCOL_TOTAL_SUCESSO]         = int(total_recorte_mod_sucesso)
            df_resultado.at[index, analisebase.DFCOL_PARTICIP]              = analisebase._dividir(total_recorte_mod, total_mod)
            df_resultado.at[index, analisebase.DFCOL_TAXA_SUCESSO]          = analisebase._dividir(total_recorte_mod_sucesso, total_recorte_mod)
            
            df_resultado.at[index, analisebase.DFCOL_META]                  = meta_recorte_mod_sucesso
            df_resultado.at[index, analisebase.DFCOL_META_MED]              = meta_recorte_mod_sucesso_med
            df_resultado.at[index, analisebase.DFCOL_META_STD]              = meta_recorte_mod_sucesso_std
            df_resultado.at[index, analisebase.DFCOL_META_MIN]              = meta_recorte_mod_sucesso_min
            df_resultado.at[index, analisebase.DFCOL_META_MAX]              = meta_recorte_mod_sucesso_max

            df_resultado.at[index, analisebase.DFCOL_ARRECADADO_SUCESSO]    = valor_recorte_mod_sucesso
            df_resultado.at[index, analisebase.DFCOL_ARRECADADO_MED]        = valor_med_recorte_mod_sucesso
            df_resultado.at[index, analisebase.DFCOL_ARRECADADO_STD]        = valor_std_recorte_mod_sucesso
            df_resultado.at[index, analisebase.DFCOL_ARRECADADO_MIN]        = valor_min_recorte_mod_sucesso
            df_resultado.at[index, analisebase.DFCOL_ARRECADADO_MAX]        = valor_max_recorte_mod_sucesso
            df_resultado.at[index, analisebase.DFCOL_APOIO_MED]             = apoio_med_recorte_mod_sucesso
            df_resultado.at[index, analisebase.DFCOL_APOIO_STD]             = apoio_std_recorte_mod_sucesso
            df_resultado.at[index, analisebase.DFCOL_APOIO_MIN]             = apoio_min_recorte_mod_sucesso
            df_resultado.at[index, analisebase.DFCOL_APOIO_MAX]             = apoio_max_recorte_mod_sucesso
            df_resultado.at[index, analisebase.DFCOL_CONTRIBUICOES]         = contribuicoes
            df_resultado.at[index, analisebase.DFCOL_CONTRIBUICOES_MED]     = contribuicoes_med
            df_resultado.at[index, analisebase.DFCOL_CONTRIBUICOES_STD]     = contribuicoes_std
            df_resultado.at[index, analisebase.DFCOL_CONTRIBUICOES_MIN]     = contribuicoes_min
            df_resultado.at[index, analisebase.DFCOL_CONTRIBUICOES_MAX]     = contribuicoes_max
            df_resultado.at[index, analisebase.DFCOL_MENOR_ANO]             = menor_ano
            df_resultado.at[index, analisebase.DFCOL_MAIOR_ANO]             = maior_ano

        # Preencher NaN com 0 para evitar problemas na divisão
        df_resultado = df_resultado.fillna(0)

        # garantir colunas int64:
        df_resultado[analisebase.DFCOL_TOTAL]           = df_resultado[analisebase.DFCOL_TOTAL].round().astype('int64')
        df_resultado[analisebase.DFCOL_TOTAL_SUCESSO]   = df_resultado[analisebase.DFCOL_TOTAL_SUCESSO].round().astype('int64')
        df_resultado[analisebase.DFCOL_CONTRIBUICOES]   = df_resultado[analisebase.DFCOL_CONTRIBUICOES].round().astype('int64')

        df_resultado[analisebase.DFCOL_MENOR_ANO]       = df_resultado[analisebase.DFCOL_MENOR_ANO].round().astype('int64')
        df_resultado[analisebase.DFCOL_MAIOR_ANO]       = df_resultado[analisebase.DFCOL_MAIOR_ANO].round().astype('int64')

        df_resultado.rename(columns={colunaslib.COL_GERAL_MODALIDADE: analisebase.DFCOL_MODALIDADE}, inplace=True)

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




