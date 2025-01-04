import analises.analise_lib as analisebase
import colunas as colunaslib
import pandas as pd
import os
import pydot
import time


CAMINHO_CSV = "../../dados/csv"
CAMINHO_TEMPLATE = f"templates"
CAMINHO_TEMPLATE_DESCRITIVO = f"{CAMINHO_TEMPLATE}/descritivo"


class CoordenadorAnaliseDescritiva(analisebase.AnaliseInterface):

    """
    Coordenar a execução da análise descritiva
    """
    def executar(self, df, ano_referencia, start_time) -> bool:

        self._start_time = start_time

        calc = analisebase.CalculosDescritivos()
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
                and self._gerar_recortes_modalidades(calc, pasta_md, pasta_img, pasta_dados)
                and self._gerar_readme(calc, pasta_md)
            )

        analisebase.marcar_andamento('\t', self._start_time)

        return resultado

    """
    Gerar o infográfico
    """
    def _gerar_infografico(self, pasta_md, pasta_img, df_resumo, df_resumo_plataforma):

        resultado = True

        print('\t\t. gerar infográfico: ', end='')

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

        analisebase.marcar_andamento_mesma_linha(self._start_time)

        print('\t\t. gerar md dos infográficos: ', end='')

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

        analisebase.marcar_andamento_mesma_linha(self._start_time)

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
    def _gerar_recortes_modalidades(self,calc, pasta_md, pasta_img, pasta_dados) -> bool:
        resultado = True
        
        print(f'\t. resumos:')
        print(f'\t\t. excel: ', end='')
        resultado = self._gerar_excel_resumo(pasta_dados, calc.df_resumo_mod)
        analisebase.marcar_andamento_mesma_linha(self._start_time)
        
        print(f'\t\t. md: ', end='')
        resultado = self._gerar_histogramas(pasta_md, pasta_img, calc.df_completo)
        resultado = self._gerar_panorama_resumo(pasta_md, pasta_img, calc.df_resumo_mod)
        analisebase.marcar_andamento_mesma_linha(self._start_time)

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

            print(f'\t\t\t. gerar md plataforma: ', end='')
            resultado = self._gerar_md_recorte(mod, pasta_md, pasta_img, df_resumo_mod_plataforma, mapa_agrupamentos['plataforma'])
            analisebase.marcar_andamento_mesma_linha(self._start_time)

            print(f'\t\t\t. gerar md gênero: ', end='')
            resultado = self._gerar_md_recorte(mod, pasta_md, pasta_img, df_resumo_mod_genero, mapa_agrupamentos['genero'])
            analisebase.marcar_andamento_mesma_linha(self._start_time)

            print(f'\t\t\t. gerar md UF: ', end='')
            resultado = self._gerar_md_recorte(mod, pasta_md, pasta_img, df_resumo_mod_uf, mapa_agrupamentos['uf'])
            analisebase.marcar_andamento_mesma_linha(self._start_time)

            print(f'\t\t\t. gerar md menções: ', end='')
            resultado = self._gerar_md_recorte(mod, pasta_md, pasta_img, df_resumo_mod_mencoes, mapa_agrupamentos['mencoes'])
            analisebase.marcar_andamento_mesma_linha(self._start_time)

            print(f'\t\t\t. gerar excel: ', end='')
            resultado = self._gerar_excel(pasta_dados, mod,
                            df_resumo_mod_plataforma,
                            df_resumo_mod_genero,
                            df_resumo_mod_uf,
                            df_resumo_mod_mencoes
                            )
            analisebase.marcar_andamento_mesma_linha(self._start_time)

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
    def _gerar_histogramas(self, pasta_md, pasta_img, df_completo):

        resultado = True

        analisebase.gerar_histograma(
            pasta_img,
            f'panorama-hist-totais-aon',
            df_completo[
                (df_completo[colunaslib.COL_GERAL_MODALIDADE] == colunaslib.CAMPANHA_AON)
                & (df_completo[colunaslib.COL_GERAL_STATUS] == colunaslib.STATUS_SUCESSO)
                ],
            250,
            colunaslib.COL_GERAL_ARRECADADO_CORRIGIDO,
            'Histograma: Valor Arrecadado Corrigido (Tudo ou Nada)',
            'Campanhas bem sucedidas',
            'Faixa de Valor Arrecadado',
            analisebase.numero_prefixo_f
        )
        analisebase.gerar_histograma(
            pasta_img,
            f'panorama-hist-totais-flex',
            df_completo[
                (df_completo[colunaslib.COL_GERAL_MODALIDADE] == colunaslib.CAMPANHA_FLEX)
                & (df_completo[colunaslib.COL_GERAL_STATUS] == colunaslib.STATUS_SUCESSO)
                ],
            250,
            colunaslib.COL_GERAL_ARRECADADO_CORRIGIDO,
            'Histograma: Valor Arrecadado Corrigido (Flex)',
            'Campanhas bem sucedidas',
            'Faixa de Valor Arrecadado',
            analisebase.numero_prefixo_f
        )
        analisebase.gerar_histograma(
            pasta_img,
            f'panorama-hist-totais-sub',
            df_completo[
                (df_completo[colunaslib.COL_GERAL_MODALIDADE] == colunaslib.CAMPANHA_SUB)
                & (df_completo[colunaslib.COL_GERAL_TOTAL_CONTRIBUICOES] != 0)
                ],
            250,
            colunaslib.COL_GERAL_ARRECADADO_CORRIGIDO,
            'Histograma: Valor Arrecadado Corrigido (Recorrente)',
            'Campanhas bem sucedidas',
            'Faixa de Valor Arrecadado',
            analisebase.numero_prefixo_f
        )
        
        analisebase.gerar_histograma(
            pasta_img,
            f'panorama-hist-meta-aon',
            df_completo[
                (df_completo[colunaslib.COL_GERAL_MODALIDADE] == colunaslib.CAMPANHA_AON)
                & (df_completo[colunaslib.COL_GERAL_STATUS] == colunaslib.STATUS_SUCESSO)
                ],
            250,
            colunaslib.COL_GERAL_META_CORRIGIDA,
            'Histograma: Meta Corrigida (Tudo ou Nada)',
            'Campanhas bem sucedidas',
            'Faixa de Meta',
            analisebase.numero_prefixo_f
        )
        
        analisebase.gerar_histograma(
            pasta_img,
            f'panorama-hist-meta-flex',
            df_completo[
                (df_completo[colunaslib.COL_GERAL_MODALIDADE] == colunaslib.CAMPANHA_FLEX)
                & (df_completo[colunaslib.COL_GERAL_STATUS] == colunaslib.STATUS_SUCESSO)
                ],
            250,
            colunaslib.COL_GERAL_META_CORRIGIDA,
            'Histograma: Meta Corrigida (Flex)',
            'Campanhas bem sucedidas',
            'Faixa de Meta',
            analisebase.numero_prefixo_f
        )
        
        analisebase.gerar_histograma(
            pasta_img,
            f'panorama-hist-meta-sub',
            df_completo[
                (df_completo[colunaslib.COL_GERAL_MODALIDADE] == colunaslib.CAMPANHA_SUB)
                & (df_completo[colunaslib.COL_GERAL_TOTAL_CONTRIBUICOES] != 0)
                ],
            250,
            colunaslib.COL_GERAL_META_CORRIGIDA,
            'Histograma: Meta Corrigida (Recorrente)',
            'Campanhas bem sucedidas',
            'Faixa de Meta',
            analisebase.numero_prefixo_f
        )
        
        analisebase.gerar_histograma(
            pasta_img,
            f'panorama-hist-contribuicoes-aon',
            df_completo[
                (df_completo[colunaslib.COL_GERAL_MODALIDADE] == colunaslib.CAMPANHA_AON)
                & (df_completo[colunaslib.COL_GERAL_STATUS] == colunaslib.STATUS_SUCESSO)
                ],
            250,
            colunaslib.COL_GERAL_TOTAL_CONTRIBUICOES,
            'Histograma: Número de Contribuições (Tudo ou Nada)',
            'Campanhas bem sucedidas',
            'Faixa de Contribuições',
            analisebase.numero_prefixo_f
        )
        
        analisebase.gerar_histograma(
            pasta_img,
            f'panorama-hist-contribuicoes-flex',
            df_completo[
                (df_completo[colunaslib.COL_GERAL_MODALIDADE] == colunaslib.CAMPANHA_FLEX)
                & (df_completo[colunaslib.COL_GERAL_STATUS] == colunaslib.STATUS_SUCESSO)
                ],
            250,
            colunaslib.COL_GERAL_TOTAL_CONTRIBUICOES,
            'Histograma: Número de Contribuições (Flex)',
            'Campanhas bem sucedidas',
            'Faixa de Contribuições',
            analisebase.numero_prefixo_f
        )
        
        analisebase.gerar_histograma(
            pasta_img,
            f'panorama-hist-contribuicoes-sub',
            df_completo[
                (df_completo[colunaslib.COL_GERAL_MODALIDADE] == colunaslib.CAMPANHA_SUB)
                & (df_completo[colunaslib.COL_GERAL_TOTAL_CONTRIBUICOES] != 0)
                ],
            250,
            colunaslib.COL_GERAL_TOTAL_CONTRIBUICOES,
            'Histograma: Número de Contribuições (Recorrente)',
            'Campanhas bem sucedidas',
            'Faixa de Contribuições',
            analisebase.numero_prefixo_f
        )

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
            analisebase.numero_inteiro_f,
            analisebase.numero_prefixo_f
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

        return resultado





