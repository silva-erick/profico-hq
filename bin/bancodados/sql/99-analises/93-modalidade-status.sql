SELECT	mc.nome modalidade
		, case mc.nome
			when 'Recorrente' then
				'por Mês'
			else
				'por Campanha'
		end periodo
		, sc.nome status
		, COUNT(1) qtd_campanhas
		, SUM(geral_arrecadado_corrigido) total_arrecadado
		, AVG(geral_arrecadado_corrigido) media_arrecadado
		, STDDEV_POP(geral_arrecadado_corrigido) desvpad_arrecadado 
		, AVG(geral_posts) media_posts
		, STDDEV_POP(geral_posts) desvpad_posts
		, AVG(geral_total_contribuicoes) media_contribuicoes
		, STDDEV_POP(geral_total_contribuicoes) desvpad_contribuicoes
		, AVG(geral_total_apoiadores) media_apoiadores
		, STDDEV_POP(geral_total_apoiadores) desvpad_apoiadores 
FROM 	Campanha c
JOIN	StatusCampanha sc
ON		sc.statuscampanha_id=c.statuscampanha_id
JOIN 	ModalidadeCampanha mc
ON		mc.modalidadecampanha_id=c.modalidadecampanha_id
GROUP 	BY mc.nome, sc.nome
ORDER 	BY 1, 2