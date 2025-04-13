WITH cte_campanhas as (
	SELECT	d.nome 			campanha_origem
			,sc.nome		campanha_status
			,mc.nome		campanha_modalidade
			,uf.acronimo	uf
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
SELECT	'Total' autor_nome, 'Total' autor_nome_publico
		, COUNT(1) qty
		, COUNT(1) filter(campanha_modalidade = 'Tudo ou Nada') tn_qty
		, SUM(geral_arrecadado_corrigido) filter(campanha_modalidade = 'Tudo ou Nada' and campanha_status != 'Falha' ) tn_tot_arrecadado
		, SUM(geral_arrecadado_corrigido) filter(campanha_modalidade = 'Tudo ou Nada' and campanha_status != 'Falha' )
			/ COUNT(1) filter(campanha_modalidade = 'Tudo ou Nada' and campanha_status != 'Falha' )
			tn_avg_arrecadado
		, MAX(geral_arrecadado_corrigido) filter(campanha_modalidade = 'Tudo ou Nada' and campanha_status != 'Falha' ) tn_max_arrecadado
		, 100.0*ROUND(COUNT(1) filter(campanha_modalidade = 'Tudo ou Nada' and campanha_status != 'Falha' )
				/ COUNT(1) filter(campanha_modalidade = 'Tudo ou Nada')
			, 3)
			tn_txsucesso
		, COUNT(1) filter(campanha_modalidade = 'Flex') flex_qty
		, SUM(geral_arrecadado_corrigido) filter(campanha_modalidade = 'Flex' and campanha_status != 'Falha' ) flex_tot_arrecadado
		, SUM(geral_arrecadado_corrigido) filter(campanha_modalidade = 'Flex' and campanha_status != 'Falha' )
			/ COUNT(1) filter(campanha_modalidade = 'Flex' and campanha_status != 'Falha' )
			flex_avg_arrecadado
		, MAX(geral_arrecadado_corrigido) filter(campanha_modalidade = 'Flex' and campanha_status != 'Falha' ) flex_max_arrecadado
		, 100.0*ROUND(COUNT(1) filter(campanha_modalidade = 'Flex' and campanha_status != 'Falha' )
				/ COUNT(1) filter(campanha_modalidade = 'Flex')
			, 3)
			flex_txsucesso
		, COUNT(1) filter(campanha_modalidade = 'Recorrente') rec_qty
		, SUM(geral_arrecadado_corrigido) filter(campanha_modalidade = 'Recorrente') rec_tot_arrecadado
		, SUM(geral_arrecadado_corrigido) filter(campanha_modalidade = 'Recorrente')
			/ COUNT(1) filter(campanha_modalidade = 'Recorrente' and geral_arrecadado_corrigido!=0)
			rec_avg_arrecadado
		, MAX(geral_arrecadado_corrigido) filter(campanha_modalidade = 'Recorrente') rec_tot_arrecadado
		, 100.0*ROUND(COUNT(1) filter(campanha_modalidade = 'Recorrente' and geral_arrecadado_corrigido!=0)
				/ COUNT(1) filter(campanha_modalidade = 'Recorrente')
			, 3)
			rec_txsucesso
FROM	cte_campanhas
UNION ALL
SELECT	autor_nome, autor_nome_publico
		, COUNT(1) qty
		, COUNT(1) filter(campanha_modalidade = 'Tudo ou Nada') tn_qty
		, SUM(geral_arrecadado_corrigido) filter(campanha_modalidade = 'Tudo ou Nada' and campanha_status != 'Falha' ) tn_tot_arrecadado
		, SUM(geral_arrecadado_corrigido) filter(campanha_modalidade = 'Tudo ou Nada' and campanha_status != 'Falha' )
			/ COUNT(1) filter(campanha_modalidade = 'Tudo ou Nada' and campanha_status != 'Falha' )
			tn_avg_arrecadado
		, MAX(geral_arrecadado_corrigido) filter(campanha_modalidade = 'Tudo ou Nada' and campanha_status != 'Falha' ) tn_max_arrecadado
		, 100.0*ROUND(COUNT(1) filter(campanha_modalidade = 'Tudo ou Nada' and campanha_status != 'Falha' )
				/ COUNT(1) filter(campanha_modalidade = 'Tudo ou Nada')
			, 3)
			tn_txsucesso
		, COUNT(1) filter(campanha_modalidade = 'Flex') flex_qty
		, SUM(geral_arrecadado_corrigido) filter(campanha_modalidade = 'Flex' and campanha_status != 'Falha' ) flex_tot_arrecadado
		, SUM(geral_arrecadado_corrigido) filter(campanha_modalidade = 'Flex' and campanha_status != 'Falha' )
			/ COUNT(1) filter(campanha_modalidade = 'Flex' and campanha_status != 'Falha' )
			flex_avg_arrecadado
		, MAX(geral_arrecadado_corrigido) filter(campanha_modalidade = 'Flex' and campanha_status != 'Falha' ) flex_max_arrecadado
		, 100.0*ROUND(COUNT(1) filter(campanha_modalidade = 'Flex' and campanha_status != 'Falha' )
				/ COUNT(1) filter(campanha_modalidade = 'Flex')
			, 3)
			flex_txsucesso
		, COUNT(1) filter(campanha_modalidade = 'Recorrente') rec_qty
		, SUM(geral_arrecadado_corrigido) filter(campanha_modalidade = 'Recorrente') rec_tot_arrecadado
		, SUM(geral_arrecadado_corrigido) filter(campanha_modalidade = 'Recorrente')
			/ COUNT(1) filter(campanha_modalidade = 'Recorrente' and geral_arrecadado_corrigido!=0)
			rec_avg_arrecadado
		, MAX(geral_arrecadado_corrigido) filter(campanha_modalidade = 'Recorrente') rec_tot_arrecadado
		, 100.0*ROUND(COUNT(1) filter(campanha_modalidade = 'Recorrente' and geral_arrecadado_corrigido!=0)
				/ COUNT(1) filter(campanha_modalidade = 'Recorrente')
			, 3)
			rec_txsucesso
FROM	cte_campanhas
GROUP	BY autor_nome, autor_nome_publico
ORDER	BY 3 desc