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
			select	cm.categoriamencao_id
			from	CategoriaMencao cm
			join	CategoriaMencaoCampanha cmc
			on		cmc.categoriamencao_id=cm.categoriamencao_id
			where	cm.nome = 'nenhuma'
			limit	1
		) IS NULL categoria_nenhuma
		,(
			select	cm.categoriamencao_id
			from	CategoriaMencao cm
			join	CategoriaMencaoCampanha cmc
			on		cmc.categoriamencao_id=cm.categoriamencao_id
			where	cm.nome = 'saloes_humor'
			limit	1
		) IS NULL categoria_saloes_humor
		,(
			select	cm.categoriamencao_id
			from	CategoriaMencao cm
			join	CategoriaMencaoCampanha cmc
			on		cmc.categoriamencao_id=cm.categoriamencao_id
			where	cm.nome = 'hqmix'
			limit	1
		) IS NULL categoria_hqmix
		,(
			select	cm.categoriamencao_id
			from	CategoriaMencao cm
			join	CategoriaMencaoCampanha cmc
			on		cmc.categoriamencao_id=cm.categoriamencao_id
			where	cm.nome = 'ccxp'
			limit	1
		) IS NULL categoria_ccxp
		,(
			select	cm.categoriamencao_id
			from	CategoriaMencao cm
			join	CategoriaMencaoCampanha cmc
			on		cmc.categoriamencao_id=cm.categoriamencao_id
			where	cm.nome = 'fiq'
			limit	1
		) IS NULL categoria_fiq
		,(
			select	cm.categoriamencao_id
			from	CategoriaMencao cm
			join	CategoriaMencaoCampanha cmc
			on		cmc.categoriamencao_id=cm.categoriamencao_id
			where	cm.nome = 'angelo_agostini'
			limit	1
		) IS NULL categoria_angelo_agostini
		,(
			select	cm.categoriamencao_id
			from	CategoriaMencao cm
			join	CategoriaMencaoCampanha cmc
			on		cmc.categoriamencao_id=cm.categoriamencao_id
			where	cm.nome = 'politica'
			limit	1
		) IS NULL categoria_politica
		,(
			select	cm.categoriamencao_id
			from	CategoriaMencao cm
			join	CategoriaMencaoCampanha cmc
			on		cmc.categoriamencao_id=cm.categoriamencao_id
			where	cm.nome = 'questoes_genero'
			limit	1
		) IS NULL categoria_questoes_genero
		,(
			select	cm.categoriamencao_id
			from	CategoriaMencao cm
			join	CategoriaMencaoCampanha cmc
			on		cmc.categoriamencao_id=cm.categoriamencao_id
			where	cm.nome = 'lgbtqiamais'
			limit	1
		) IS NULL categoria_lgbtqiamais
		,(
			select	cm.categoriamencao_id
			from	CategoriaMencao cm
			join	CategoriaMencaoCampanha cmc
			on		cmc.categoriamencao_id=cm.categoriamencao_id
			where	cm.nome = 'terror'
			limit	1
		) IS NULL categoria_terror
		,(
			select	cm.categoriamencao_id
			from	CategoriaMencao cm
			join	CategoriaMencaoCampanha cmc
			on		cmc.categoriamencao_id=cm.categoriamencao_id
			where	cm.nome = 'humor'
			limit	1
		) IS NULL categoria_humor
		,(
			select	cm.categoriamencao_id
			from	CategoriaMencao cm
			join	CategoriaMencaoCampanha cmc
			on		cmc.categoriamencao_id=cm.categoriamencao_id
			where	cm.nome = 'herois'
			limit	1
		) IS NULL categoria_herois
		,(
			select	cm.categoriamencao_id
			from	CategoriaMencao cm
			join	CategoriaMencaoCampanha cmc
			on		cmc.categoriamencao_id=cm.categoriamencao_id
			where	cm.nome = 'disputa'
			limit	1
		) IS NULL categoria_disputa
		,(
			select	cm.categoriamencao_id
			from	CategoriaMencao cm
			join	CategoriaMencaoCampanha cmc
			on		cmc.categoriamencao_id=cm.categoriamencao_id
			where	cm.nome = 'ficcao_cientifica'
			limit	1
		) IS NULL categoria_ficcao_cientifica
		,(
			select	cm.categoriamencao_id
			from	CategoriaMencao cm
			join	CategoriaMencaoCampanha cmc
			on		cmc.categoriamencao_id=cm.categoriamencao_id
			where	cm.nome = 'fantasia'
			limit	1
		) IS NULL categoria_fantasia
		,(
			select	cm.categoriamencao_id
			from	CategoriaMencao cm
			join	CategoriaMencaoCampanha cmc
			on		cmc.categoriamencao_id=cm.categoriamencao_id
			where	cm.nome = 'folclore'
			limit	1
		) IS NULL categoria_folclore
		,(
			select	cm.categoriamencao_id
			from	CategoriaMencao cm
			join	CategoriaMencaoCampanha cmc
			on		cmc.categoriamencao_id=cm.categoriamencao_id
			where	cm.nome = 'zine'
			limit	1
		) IS NULL categoria_zine
		,(
			select	cm.categoriamencao_id
			from	CategoriaMencao cm
			join	CategoriaMencaoCampanha cmc
			on		cmc.categoriamencao_id=cm.categoriamencao_id
			where	cm.nome = 'webformatos'
			limit	1
		) IS NULL categoria_webformatos
		,(
			select	cm.categoriamencao_id
			from	CategoriaMencao cm
			join	CategoriaMencaoCampanha cmc
			on		cmc.categoriamencao_id=cm.categoriamencao_id
			where	cm.nome = 'erotismo'
			limit	1
		) IS NULL categoria_erotismo
		,(
			select	cm.categoriamencao_id
			from	CategoriaMencao cm
			join	CategoriaMencaoCampanha cmc
			on		cmc.categoriamencao_id=cm.categoriamencao_id
			where	cm.nome = 'religiosidade'
			limit	1
		) IS NULL categoria_religiosidade
		,(
			select	cm.categoriamencao_id
			from	CategoriaMencao cm
			join	CategoriaMencaoCampanha cmc
			on		cmc.categoriamencao_id=cm.categoriamencao_id
			where	cm.nome = 'jogos'
			limit	1
		) IS NULL categoria_jogos
		,(
			select	cm.categoriamencao_id
			from	CategoriaMencao cm
			join	CategoriaMencaoCampanha cmc
			on		cmc.categoriamencao_id=cm.categoriamencao_id
			where	cm.nome = 'midia_independente'
			limit	1
		) IS NULL categoria_midia_independente
FROM	cte_campanhas c
