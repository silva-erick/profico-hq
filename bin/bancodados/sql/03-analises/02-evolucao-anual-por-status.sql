SELECT	extract (year from geral_data_ini) ano
		,mc.nome modalidade
		, case mc.nome
			when 'Recorrente' then
				'por Mês'
			else
				'por Campanha'
		end periodo
		, sc.nome status
		, COUNT(1) qtd_campanhas
FROM 	Campanha c
JOIN	StatusCampanha sc
ON		sc.statuscampanha_id=c.statuscampanha_id
JOIN 	ModalidadeCampanha mc
ON		mc.modalidadecampanha_id=c.modalidadecampanha_id
GROUP 	BY extract (year from geral_data_ini), mc.nome, sc.nome
ORDER 	BY 1, 2