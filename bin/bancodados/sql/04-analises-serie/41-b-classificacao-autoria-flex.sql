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
			,c.*
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
,cte_campanhas_analise as (
	SELECT	ano
		, autor_classificacao
		, count(1) qtd
		, SUM(geral_arrecadado_corrigido) filter( campanha_status != 'Falha' ) tot_arrecadado
		, SUM(geral_arrecadado_corrigido) filter( campanha_status != 'Falha' )
			/ COUNT(1) filter( campanha_status != 'Falha' )
			avg_arrecadado
		, MAX(geral_arrecadado_corrigido) filter( campanha_status != 'Falha' ) max_arrecadado
		,100.0*ROUND(COUNT(1) filter( campanha_status != 'Falha' )
				/ COUNT(1)
			, 3)
		txsucesso
	FROM	cte_campanhas
	WHERE	campanha_modalidade='Flex'
	GROUP	BY ano, autor_classificacao
)
PIVOT	cte_campanhas_analise
ON		autor_classificacao
USING	sum(qtd) qtd
		,sum(tot_arrecadado) tot_arrecadado
		,sum(avg_arrecadado) avg_arrecadado
		,sum(max_arrecadado) max_arrecadado
		,sum(txsucesso) txsucesso
GROUP	BY ano;