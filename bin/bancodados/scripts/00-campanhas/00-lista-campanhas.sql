WITH cte_campanhas as (
	SELECT	d.nome 			campanha_origem
			,IF(geral_arrecadado_corrigido=0, 'Falha', sc.nome) campanha_status
			,mc.nome		campanha_modalidade
			,COALESCE(uf.acronimo,'XX')	uf
			,m.nome			municipio
			,extract(year from geral_data_ini)	ano
			,ca.nome		autor_classificacao
			,a.nome			autor_nome
			,a.nome_publico	autor_nome_publico
			,c.campanha_id
			,c.origemdados_id
			,c.original_id
			,c.recompensas_menor_nominal
			,c.recompensas_menor_ajustado
			,c.recompensas_quantidade
			,c.social_seguidores
			,c.social_newsletter
			,c.social_sub_contribuicoes_amigos
			,c.social_sub_novos_seguidores
			,c.social_sub_posts_projeto
			,c.social_projetos_contribuidos
			,c.social_projetos_publicados
			,c.municipio_id
			,c.geral_content_rating
			,c.geral_contributed_by_friends
			,c.geral_capa_imagem
			,c.geral_capa_video
			,c.geral_dias_campanha
			,c.geral_data_fim
			,c.geral_data_ini
			,c.geral_meta
			,c.geral_meta_corrigida
			,c.geral_arrecadado
			,c.geral_arrecadado_corrigido
			,c.geral_percentual_arrecadado
			,c.geral_conteudo_adulto
			,c.geral_posts
			,c.modalidadecampanha_id
			,c.geral_titulo
			,c.statuscampanha_id
			,c.geral_total_contribuicoes
			,c.geral_total_apoiadores
			--,c.geral_sobre
	FROM	Campanha c
	JOIN	OrigemDados d
	ON		d.origemdados_id=c.origemdados_id
	JOIN	ModalidadeCampanha mc
	ON		mc.modalidadecampanha_id=c.modalidadecampanha_id
	JOIN	StatusCampanha sc
	ON 		sc.statuscampanha_id=c.statuscampanha_id
	JOIN	Autor a
	ON		a.autor_id=c.autor_id
	JOIN	ClassificacaoAutor ca
	ON		ca.classificacaoautor_id=a.classificacaoautor_id
	LEFT	JOIN	Municipio m
	ON		m.municipio_id=c.municipio_id
	LEFT	JOIN	UnidadeFederativa uf
	ON 		uf.uf_id=m.uf_id
)
SELECT		c.*
		, (
			SELECT	cmc.categoriamencao_id
			FROM	CategoriaMencaoCampanha cmc
			WHERE	cmc.campanha_id=c.campanha_id
			AND		cmc.categoriamencao_id=-1
			LIMIT	1
		) IS NULL categoria_nenhuma
		,(
			SELECT	cmc.categoriamencao_id
			FROM	CategoriaMencaoCampanha cmc
			WHERE	cmc.campanha_id=c.campanha_id
			AND		cmc.categoriamencao_id=1
			LIMIT	1
		) IS NULL categoria_saloes_humor
		,(
			SELECT	cmc.categoriamencao_id
			FROM	CategoriaMencaoCampanha cmc
			WHERE	cmc.campanha_id=c.campanha_id
			AND		cmc.categoriamencao_id=2
			LIMIT	1
		) IS NULL categoria_hqmix
		,(
			SELECT	cmc.categoriamencao_id
			FROM	CategoriaMencaoCampanha cmc
			WHERE	cmc.campanha_id=c.campanha_id
			AND		cmc.categoriamencao_id=3
			LIMIT	1
		) IS NULL categoria_ccxp
		,(
			SELECT	cmc.categoriamencao_id
			FROM	CategoriaMencaoCampanha cmc
			WHERE	cmc.campanha_id=c.campanha_id
			AND		cmc.categoriamencao_id=4
			LIMIT	1
		) IS NULL categoria_fiq
		,(
			SELECT	cmc.categoriamencao_id
			FROM	CategoriaMencaoCampanha cmc
			WHERE	cmc.campanha_id=c.campanha_id
			AND		cmc.categoriamencao_id=5
			LIMIT	1
		) IS NULL categoria_angelo_agostini
		,(
			SELECT	cmc.categoriamencao_id
			FROM	CategoriaMencaoCampanha cmc
			WHERE	cmc.campanha_id=c.campanha_id
			AND		cmc.categoriamencao_id=6
			LIMIT	1
		) IS NULL categoria_politica
		,(
			SELECT	cmc.categoriamencao_id
			FROM	CategoriaMencaoCampanha cmc
			WHERE	cmc.campanha_id=c.campanha_id
			AND		cmc.categoriamencao_id=7
			LIMIT	1
		) IS NULL categoria_questoes_genero
		,(
			SELECT	cmc.categoriamencao_id
			FROM	CategoriaMencaoCampanha cmc
			WHERE	cmc.campanha_id=c.campanha_id
			AND		cmc.categoriamencao_id=8
			LIMIT	1
		) IS NULL categoria_lgbtqiamais
		,(
			SELECT	cmc.categoriamencao_id
			FROM	CategoriaMencaoCampanha cmc
			WHERE	cmc.campanha_id=c.campanha_id
			AND		cmc.categoriamencao_id=9
			LIMIT	1
		) IS NULL categoria_terror
		,(
			SELECT	cmc.categoriamencao_id
			FROM	CategoriaMencaoCampanha cmc
			WHERE	cmc.campanha_id=c.campanha_id
			AND		cmc.categoriamencao_id=10
			LIMIT	1
		) IS NULL categoria_humor
		,(
			SELECT	cmc.categoriamencao_id
			FROM	CategoriaMencaoCampanha cmc
			WHERE	cmc.campanha_id=c.campanha_id
			AND		cmc.categoriamencao_id=11
			LIMIT	1
		) IS NULL categoria_herois
		,(
			SELECT	cmc.categoriamencao_id
			FROM	CategoriaMencaoCampanha cmc
			WHERE	cmc.campanha_id=c.campanha_id
			AND		cmc.categoriamencao_id=12
			LIMIT	1
		) IS NULL categoria_disputa
		,(
			SELECT	cmc.categoriamencao_id
			FROM	CategoriaMencaoCampanha cmc
			WHERE	cmc.campanha_id=c.campanha_id
			AND		cmc.categoriamencao_id=13
			LIMIT	1
		) IS NULL categoria_ficcao_cientifica
		,(
			SELECT	cmc.categoriamencao_id
			FROM	CategoriaMencaoCampanha cmc
			WHERE	cmc.campanha_id=c.campanha_id
			AND		cmc.categoriamencao_id=14
			LIMIT	1
		) IS NULL categoria_fantasia
		,(
			SELECT	cmc.categoriamencao_id
			FROM	CategoriaMencaoCampanha cmc
			WHERE	cmc.campanha_id=c.campanha_id
			AND		cmc.categoriamencao_id=15
			LIMIT	1
		) IS NULL categoria_folclore
		,(
			SELECT	cmc.categoriamencao_id
			FROM	CategoriaMencaoCampanha cmc
			WHERE	cmc.campanha_id=c.campanha_id
			AND		cmc.categoriamencao_id=16
			LIMIT	1
		) IS NULL categoria_zine
		,(
			SELECT	cmc.categoriamencao_id
			FROM	CategoriaMencaoCampanha cmc
			WHERE	cmc.campanha_id=c.campanha_id
			AND		cmc.categoriamencao_id=17
			LIMIT	1
		) IS NULL categoria_webformatos
		,(
			SELECT	cmc.categoriamencao_id
			FROM	CategoriaMencaoCampanha cmc
			WHERE	cmc.campanha_id=c.campanha_id
			AND		cmc.categoriamencao_id=18
			LIMIT	1
		) IS NULL categoria_erotismo
		,(
			SELECT	cmc.categoriamencao_id
			FROM	CategoriaMencaoCampanha cmc
			WHERE	cmc.campanha_id=c.campanha_id
			AND		cmc.categoriamencao_id=19
			LIMIT	1
		) IS NULL categoria_religiosidade
		,(
			SELECT	cmc.categoriamencao_id
			FROM	CategoriaMencaoCampanha cmc
			WHERE	cmc.campanha_id=c.campanha_id
			AND		cmc.categoriamencao_id=20
			LIMIT	1
		) IS NULL categoria_jogos
		,(
			SELECT	cmc.categoriamencao_id
			FROM	CategoriaMencaoCampanha cmc
			WHERE	cmc.campanha_id=c.campanha_id
			AND		cmc.categoriamencao_id=21
			LIMIT	1
		) IS NULL categoria_midia_independente
FROM	cte_campanhas c