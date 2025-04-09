/*
 * A análise por modalidade aponta que
 */
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
SELECT	'ano de início' as 'variável'
		,min(ano) as Todos
		,min(ano) filter (campanha_origem='Catarse') as 'Catarse'
		,min(ano) filter (campanha_origem='Apoia.se') as 'Apoia.se'
FROM	cte_campanhas
UNION ALL
SELECT	'campanhas' as 'variável'
		,count(1) as Todos
		,count(1) filter (campanha_origem='Catarse') as 'Catarse'
		,count(1) filter (campanha_origem='Apoia.se') as 'Apoia.se'
FROM	cte_campanhas
UNION ALL
SELECT	'campanhas: tudo ou nada' parâmetro
		,count(1) filter (campanha_modalidade='Tudo ou Nada')
		,count(1) filter (campanha_modalidade='Tudo ou Nada' and campanha_origem='Catarse')
		,count(1) filter (campanha_modalidade='Tudo ou Nada' and campanha_origem='Apoia.se')
FROM	cte_campanhas
UNION ALL
SELECT	'campanhas: flex' parâmetro
		,count(1) filter (campanha_modalidade='Flex')
		,count(1) filter (campanha_modalidade='Flex' and campanha_origem='Catarse')
		,count(1) filter (campanha_modalidade='Flex' and campanha_origem='Apoia.se')
FROM	cte_campanhas
UNION ALL
SELECT	'campanhas: recorrente' parâmetro
		,count(1) filter (campanha_modalidade='Recorrente')
		,count(1) filter (campanha_modalidade='Recorrente' and campanha_origem='Catarse')
		,count(1) filter (campanha_modalidade='Recorrente' and campanha_origem='Apoia.se')
FROM	cte_campanhas
UNION ALL
SELECT	'movimentação (por campanha)' parâmetro
		,sum(geral_arrecadado_corrigido) filter (campanha_modalidade in ('Tudo ou Nada', 'Flex') )
		,sum(geral_arrecadado_corrigido) filter (campanha_modalidade in ('Tudo ou Nada', 'Flex') and campanha_origem='Catarse')
		,sum(geral_arrecadado_corrigido) filter (campanha_modalidade in ('Tudo ou Nada', 'Flex') and campanha_origem='Apoia.se')
FROM	cte_campanhas
UNION ALL
SELECT	'movimentação: tudo ou nada (por campanha)' parâmetro
		,sum(geral_arrecadado_corrigido) filter (campanha_modalidade='Tudo ou Nada')
		,sum(geral_arrecadado_corrigido) filter (campanha_modalidade='Tudo ou Nada' and campanha_origem='Catarse')
		,sum(geral_arrecadado_corrigido) filter (campanha_modalidade='Tudo ou Nada' and campanha_origem='Apoia.se')
FROM	cte_campanhas
UNION ALL
SELECT	'movimentação: flex (por campanha)' parâmetro
		,sum(geral_arrecadado_corrigido) filter (campanha_modalidade='Flex')
		,sum(geral_arrecadado_corrigido) filter (campanha_modalidade='Flex' and campanha_origem='Catarse')
		,sum(geral_arrecadado_corrigido) filter (campanha_modalidade='Flex' and campanha_origem='Apoia.se')
FROM	cte_campanhas
UNION ALL
SELECT	'movimentação: recorrente (por mês)' parâmetro
		,sum(geral_arrecadado_corrigido) filter (campanha_modalidade='Recorrente')
		,sum(geral_arrecadado_corrigido) filter (campanha_modalidade='Recorrente' and campanha_origem='Catarse')
		,sum(geral_arrecadado_corrigido) filter (campanha_modalidade='Recorrente' and campanha_origem='Apoia.se')
FROM	cte_campanhas
UNION ALL
SELECT	'taxa de sucesso (%)' as 'variável'
		,100*count(1) filter (campanha_status in ('Sucesso', 'Aguardando Fundos') ) / count(1) filter (campanha_status in ('Sucesso', 'Aguardando Fundos','Falha') )
		,100*count(1) filter (campanha_status in ('Sucesso', 'Aguardando Fundos') and campanha_origem='Catarse') / count(1) filter (campanha_status in ('Sucesso', 'Aguardando Fundos','Falha') and campanha_origem='Catarse')
		,100*count(1) filter (campanha_status in ('Sucesso', 'Aguardando Fundos') and campanha_origem='Apoia.se') / count(1) filter (campanha_status in ('Sucesso', 'Aguardando Fundos','Falha') and campanha_origem='Apoia.se')
FROM	cte_campanhas
UNION ALL
SELECT	'taxa de sucesso: tudo ou nada (%)' as 'variável'
		,100*count(1) filter (campanha_modalidade='Tudo ou Nada' and campanha_status in ('Sucesso', 'Aguardando Fundos') ) / count(1) filter (campanha_modalidade='Tudo ou Nada' and campanha_status in ('Sucesso', 'Aguardando Fundos','Falha') )
		,100*count(1) filter (campanha_modalidade='Tudo ou Nada' and campanha_status in ('Sucesso', 'Aguardando Fundos') and campanha_origem='Catarse') / count(1) filter (campanha_modalidade='Tudo ou Nada' and campanha_status in ('Sucesso', 'Aguardando Fundos','Falha') and campanha_origem='Catarse')
		,
			case
				when 0 = count(1) filter (campanha_modalidade='Tudo ou Nada' and campanha_status in ('Sucesso', 'Aguardando Fundos','Falha') and campanha_origem='Apoia.se') then
					NULL
				else
					100*count(1) filter (campanha_modalidade='Tudo ou Nada' and campanha_status in ('Sucesso', 'Aguardando Fundos') and campanha_origem='Apoia.se') / count(1) filter (campanha_modalidade='Tudo ou Nada' and campanha_status in ('Sucesso', 'Aguardando Fundos','Falha') and campanha_origem='Apoia.se')
			end
FROM	cte_campanhas
UNION ALL
SELECT	'taxa de sucesso: flex (%)' as 'variável'
		,100*count(1) filter (campanha_modalidade='Flex' and campanha_status in ('Sucesso', 'Aguardando Fundos') ) / count(1) filter (campanha_modalidade='Flex' and campanha_status in ('Sucesso', 'Aguardando Fundos','Falha') )
		,100*count(1) filter (campanha_modalidade='Flex' and campanha_status in ('Sucesso', 'Aguardando Fundos') and campanha_origem='Catarse') / count(1) filter (campanha_modalidade='Flex' and campanha_status in ('Sucesso', 'Aguardando Fundos','Falha') and campanha_origem='Catarse')
		,100*count(1) filter (campanha_modalidade='Flex' and campanha_status in ('Sucesso', 'Aguardando Fundos') and campanha_origem='Apoia.se') / count(1) filter (campanha_modalidade='Flex' and campanha_status in ('Sucesso', 'Aguardando Fundos','Falha') and campanha_origem='Apoia.se')
FROM	cte_campanhas
UNION ALL
SELECT	'arrecadação (por campanha)'
		,round(sum(geral_arrecadado_corrigido) filter (campanha_modalidade in ('Tudo ou Nada', 'Flex')  and campanha_status in ('Sucesso', 'Aguardando Fundos')), 2)
		,round(sum(geral_arrecadado_corrigido) filter (campanha_modalidade in ('Tudo ou Nada', 'Flex') and campanha_origem='Catarse' and campanha_status in ('Sucesso', 'Aguardando Fundos')), 2)
		,round(sum(geral_arrecadado_corrigido) filter (campanha_modalidade in ('Tudo ou Nada', 'Flex') and campanha_origem='Apoia.se' and campanha_status in ('Sucesso', 'Aguardando Fundos')), 2)
FROM	cte_campanhas
UNION ALL
SELECT	'arrecadação: tudo ou nada (por campanha)'
		,round(sum(geral_arrecadado_corrigido) filter (campanha_modalidade='Tudo ou Nada' and campanha_status in ('Sucesso', 'Aguardando Fundos')), 2)
		,round(sum(geral_arrecadado_corrigido) filter (campanha_modalidade='Tudo ou Nada' and campanha_origem='Catarse' and campanha_status in ('Sucesso', 'Aguardando Fundos')), 2)
		,round(sum(geral_arrecadado_corrigido) filter (campanha_modalidade='Tudo ou Nada' and campanha_origem='Apoia.se' and campanha_status in ('Sucesso', 'Aguardando Fundos')), 2)
FROM	cte_campanhas
UNION ALL
SELECT	'arrecadação: flex (por campanha)'
		,round(sum(geral_arrecadado_corrigido) filter (campanha_modalidade='Flex' and campanha_status in ('Sucesso', 'Aguardando Fundos')), 2)
		,round(sum(geral_arrecadado_corrigido) filter (campanha_modalidade='Flex' and campanha_origem='Catarse' and campanha_status in ('Sucesso', 'Aguardando Fundos')), 2)
		,round(sum(geral_arrecadado_corrigido) filter (campanha_modalidade='Flex' and campanha_origem='Apoia.se' and campanha_status in ('Sucesso', 'Aguardando Fundos')), 2)
FROM	cte_campanhas
UNION ALL
SELECT	'arrecadação: recorrente (por mês)'
		,round(sum(geral_arrecadado_corrigido) filter (campanha_modalidade='Recorrente' and campanha_status in ('Sucesso', 'Aguardando Fundos', 'Publicado')), 2)
		,round(sum(geral_arrecadado_corrigido) filter (campanha_modalidade='Recorrente' and campanha_origem='Catarse' and campanha_status in ('Sucesso', 'Aguardando Fundos', 'Publicado')), 2)
		,round(sum(geral_arrecadado_corrigido) filter (campanha_modalidade='Recorrente' and campanha_origem='Apoia.se' and campanha_status in ('Sucesso', 'Aguardando Fundos', 'Publicado')), 2)
FROM	cte_campanhas


/*
variável	Todos	Catarse	Apoia.se
ano de início	2,011	2,011	2,016
campanhas	4,045	3,300	745
campanhas: tudo ou nada	1,479	1,479	0
campanhas: flex	1,762	1,750	12
campanhas: recorrente	804	71	733
movimentação (por campanha)	52,264,997.998	52,263,844.325	1,153.673
movimentação: tudo ou nada (por campanha)	29,551,287.868	29,551,287.868	[NULL]
movimentação: flex (por campanha)	22,713,710.13	22,712,556.457	1,153.673
movimentação: recorrente (por mês)	46,701.511	3,862.125	42,839.386
taxa de sucesso (%)	80.404589372	80.6363636364	16.6666666667
taxa de sucesso: tudo ou nada (%)	62.4746450304	62.4746450304	[NULL]
taxa de sucesso: flex (%)	94.665153235	95.2	16.6666666667
arrecadação (por campanha)	50,519,101.56	50,517,963.11	1,138.45
arrecadação: tudo ou nada (por campanha)	27,805,556.58	27,805,556.58	[NULL]
arrecadação: flex (por campanha)	22,713,544.98	22,712,406.53	1,138.45
arrecadação: recorrente (por mês)	46,701.51	3,862.13	42,839.39
**/