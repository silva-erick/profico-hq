WITH cte_campanhas as (
	SELECT	d.nome 			campanha_origem
			,IF(geral_arrecadado_corrigido=0, 'Falha', sc.nome) campanha_status
			,mc.nome		campanha_modalidade
			,uf.acronimo	uf
			,extract(year from geral_data_ini) ano
			,m.nome			municipio
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
, cte_analises as (
	PIVOT	cte_campanhas
	ON		uf
	USING	COUNT(1)
	GROUP	BY ano
)
select	*
from	cte_analises
ORDER	BY ano asc