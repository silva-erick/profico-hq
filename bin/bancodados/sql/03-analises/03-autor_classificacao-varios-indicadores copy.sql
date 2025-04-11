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
		,min(ano) filter (autor_classificacao='Empresa') as 'empresa'
		,min(ano) filter (autor_classificacao='Coletivo') as 'coletivo'
		,min(ano) filter (autor_classificacao='Feminino') as 'feminino'
		,min(ano) filter (autor_classificacao='Masculino') as 'masculino'
		,min(ano) filter (autor_classificacao='Outros') as 'outros'
		,min(ano) as Todos
FROM	cte_campanhas
UNION ALL
SELECT	'campanhas' as 'variável'
		,count(1) filter (autor_classificacao='Empresa')
		,count(1) filter (autor_classificacao='Coletivo')
		,count(1) filter (autor_classificacao='Feminino')
		,count(1) filter (autor_classificacao='Masculino')
		,count(1) filter (autor_classificacao='Outros')
		,count(1)
FROM	cte_campanhas
UNION ALL
SELECT	'campanhas: plataforma:catarse' parâmetro
		,count(1) filter (campanha_origem='Catarse' and autor_classificacao='Empresa')
		,count(1) filter (campanha_origem='Catarse' and autor_classificacao='Coletivo')
		,count(1) filter (campanha_origem='Catarse' and autor_classificacao='Feminino')
		,count(1) filter (campanha_origem='Catarse' and autor_classificacao='Masculino')
		,count(1) filter (campanha_origem='Catarse' and autor_classificacao='Outros')
		,count(1) filter (campanha_origem='Catarse')
FROM	cte_campanhas
UNION ALL
SELECT	'campanhas: plataforma:apoia.se' parâmetro
		,count(1) filter (campanha_origem='Apoia.se' and autor_classificacao='Empresa')
		,count(1) filter (campanha_origem='Apoia.se' and autor_classificacao='Coletivo')
		,count(1) filter (campanha_origem='Apoia.se' and autor_classificacao='Feminino')
		,count(1) filter (campanha_origem='Apoia.se' and autor_classificacao='Masculino')
		,count(1) filter (campanha_origem='Apoia.se' and autor_classificacao='Outros')
		,count(1) filter (campanha_origem='Apoia.se')
FROM	cte_campanhas
UNION ALL
SELECT	'campanhas: tudo ou nada' parâmetro
		,count(1) filter (campanha_modalidade='Tudo ou Nada' and autor_classificacao='Empresa')
		,count(1) filter (campanha_modalidade='Tudo ou Nada' and autor_classificacao='Coletivo')
		,count(1) filter (campanha_modalidade='Tudo ou Nada' and autor_classificacao='Feminino')
		,count(1) filter (campanha_modalidade='Tudo ou Nada' and autor_classificacao='Masculino')
		,count(1) filter (campanha_modalidade='Tudo ou Nada' and autor_classificacao='Outros')
		,count(1) filter (campanha_modalidade='Tudo ou Nada')
FROM	cte_campanhas
UNION ALL
SELECT	'campanhas: flex' parâmetro
		,count(1) filter (campanha_modalidade='Flex' and autor_classificacao='Empresa')
		,count(1) filter (campanha_modalidade='Flex' and autor_classificacao='Coletivo')
		,count(1) filter (campanha_modalidade='Flex' and autor_classificacao='Feminino')
		,count(1) filter (campanha_modalidade='Flex' and autor_classificacao='Masculino')
		,count(1) filter (campanha_modalidade='Flex' and autor_classificacao='Outros')
		,count(1) filter (campanha_modalidade='Flex')
FROM	cte_campanhas
UNION ALL
SELECT	'campanhas: recorrente' parâmetro
		,count(1) filter (campanha_modalidade='Recorrente' and autor_classificacao='Empresa')
		,count(1) filter (campanha_modalidade='Recorrente' and autor_classificacao='Coletivo')
		,count(1) filter (campanha_modalidade='Recorrente' and autor_classificacao='Feminino')
		,count(1) filter (campanha_modalidade='Recorrente' and autor_classificacao='Masculino')
		,count(1) filter (campanha_modalidade='Recorrente' and autor_classificacao='Outros')
		,count(1) filter (campanha_modalidade='Recorrente')
FROM	cte_campanhas
UNION ALL
SELECT	'movimentação (por campanha)' parâmetro
		,round(sum(geral_arrecadado_corrigido) filter (campanha_modalidade in ('Tudo ou Nada', 'Flex') and autor_classificacao='Empresa'), 2)
		,round(sum(geral_arrecadado_corrigido) filter (campanha_modalidade in ('Tudo ou Nada', 'Flex') and autor_classificacao='Coletivo'), 2)
		,round(sum(geral_arrecadado_corrigido) filter (campanha_modalidade in ('Tudo ou Nada', 'Flex') and autor_classificacao='Feminino'), 2)
		,round(sum(geral_arrecadado_corrigido) filter (campanha_modalidade in ('Tudo ou Nada', 'Flex') and autor_classificacao='Masculino'), 2)
		,round(sum(geral_arrecadado_corrigido) filter (campanha_modalidade in ('Tudo ou Nada', 'Flex') and autor_classificacao='Outros'), 2)
		,round(sum(geral_arrecadado_corrigido) filter (campanha_modalidade in ('Tudo ou Nada', 'Flex') ), 2)
FROM	cte_campanhas
UNION ALL
SELECT	'movimentação: tudo ou nada (por campanha)' parâmetro
		,round(sum(geral_arrecadado_corrigido) filter (campanha_modalidade='Tudo ou Nada' and autor_classificacao='Empresa'), 2)
		,round(sum(geral_arrecadado_corrigido) filter (campanha_modalidade='Tudo ou Nada' and autor_classificacao='Coletivo'), 2)
		,round(sum(geral_arrecadado_corrigido) filter (campanha_modalidade='Tudo ou Nada' and autor_classificacao='Feminino'), 2)
		,round(sum(geral_arrecadado_corrigido) filter (campanha_modalidade='Tudo ou Nada' and autor_classificacao='Masculino'), 2)
		,round(sum(geral_arrecadado_corrigido) filter (campanha_modalidade='Tudo ou Nada' and autor_classificacao='Outros'), 2)
		,round(sum(geral_arrecadado_corrigido) filter (campanha_modalidade='Tudo ou Nada'), 2)
FROM	cte_campanhas
UNION ALL
SELECT	'movimentação: flex (por campanha)' parâmetro
		,round(sum(geral_arrecadado_corrigido) filter (campanha_modalidade='Flex' and autor_classificacao='Empresa'), 2)
		,round(sum(geral_arrecadado_corrigido) filter (campanha_modalidade='Flex' and autor_classificacao='Coletivo'), 2)
		,round(sum(geral_arrecadado_corrigido) filter (campanha_modalidade='Flex' and autor_classificacao='Feminino'), 2)
		,round(sum(geral_arrecadado_corrigido) filter (campanha_modalidade='Flex' and autor_classificacao='Masculino'), 2)
		,round(sum(geral_arrecadado_corrigido) filter (campanha_modalidade='Flex' and autor_classificacao='Outros'), 2)
		,round(sum(geral_arrecadado_corrigido) filter (campanha_modalidade='Flex'), 2)
FROM	cte_campanhas
UNION ALL
SELECT	'movimentação: recorrente (por mês)' parâmetro
		,round(sum(geral_arrecadado_corrigido) filter (campanha_modalidade='Recorrente' and autor_classificacao='Empresa'), 2)
		,round(sum(geral_arrecadado_corrigido) filter (campanha_modalidade='Recorrente' and autor_classificacao='Coletivo'), 2)
		,round(sum(geral_arrecadado_corrigido) filter (campanha_modalidade='Recorrente' and autor_classificacao='Feminino'), 2)
		,round(sum(geral_arrecadado_corrigido) filter (campanha_modalidade='Recorrente' and autor_classificacao='Masculino'), 2)
		,round(sum(geral_arrecadado_corrigido) filter (campanha_modalidade='Recorrente' and autor_classificacao='Outros'), 2)
		,round(sum(geral_arrecadado_corrigido) filter (campanha_modalidade='Recorrente'), 2)
FROM	cte_campanhas
UNION ALL
SELECT	'taxa de sucesso (%)' as 'variável'
		,round(100*count(1) filter (campanha_status in ('Sucesso', 'Aguardando Fundos') and autor_classificacao='Empresa') / count(1) filter (campanha_status in ('Sucesso', 'Aguardando Fundos','Falha') and autor_classificacao='Empresa'), 2)
		,round(100*count(1) filter (campanha_status in ('Sucesso', 'Aguardando Fundos') and autor_classificacao='Coletivo') / count(1) filter (campanha_status in ('Sucesso', 'Aguardando Fundos','Falha') and autor_classificacao='Coletivo'), 2)
		,round(100*count(1) filter (campanha_status in ('Sucesso', 'Aguardando Fundos') and autor_classificacao='Feminino') / count(1) filter (campanha_status in ('Sucesso', 'Aguardando Fundos','Falha') and autor_classificacao='Feminino'), 2)
		,round(100*count(1) filter (campanha_status in ('Sucesso', 'Aguardando Fundos') and autor_classificacao='Masculino') / count(1) filter (campanha_status in ('Sucesso', 'Aguardando Fundos','Falha') and autor_classificacao='Masculino'), 2)
		,round(100*count(1) filter (campanha_status in ('Sucesso', 'Aguardando Fundos') and autor_classificacao='Outros') / count(1) filter (campanha_status in ('Sucesso', 'Aguardando Fundos','Falha') and autor_classificacao='Outros'), 2)
		,round(100*count(1) filter (campanha_status in ('Sucesso', 'Aguardando Fundos') ) / count(1) filter (campanha_status in ('Sucesso', 'Aguardando Fundos','Falha') ), 2)
FROM	cte_campanhas
UNION ALL
SELECT	'taxa de sucesso: tudo ou nada (%)' as 'variável'
		,round(100*count(1) filter (campanha_modalidade='Tudo ou Nada' and campanha_status in ('Sucesso', 'Aguardando Fundos') and autor_classificacao='Empresa') / count(1) filter (campanha_modalidade='Tudo ou Nada' and campanha_status in ('Sucesso', 'Aguardando Fundos','Falha') and autor_classificacao='Empresa'), 2)
		,round(100*count(1) filter (campanha_modalidade='Tudo ou Nada' and campanha_status in ('Sucesso', 'Aguardando Fundos') and autor_classificacao='Coletivo') / count(1) filter (campanha_modalidade='Tudo ou Nada' and campanha_status in ('Sucesso', 'Aguardando Fundos','Falha') and autor_classificacao='Coletivo'), 2)
		,round(100*count(1) filter (campanha_modalidade='Tudo ou Nada' and campanha_status in ('Sucesso', 'Aguardando Fundos') and autor_classificacao='Feminino') / count(1) filter (campanha_modalidade='Tudo ou Nada' and campanha_status in ('Sucesso', 'Aguardando Fundos','Falha') and autor_classificacao='Feminino'), 2)
		,round(100*count(1) filter (campanha_modalidade='Tudo ou Nada' and campanha_status in ('Sucesso', 'Aguardando Fundos') and autor_classificacao='Masculino') / count(1) filter (campanha_modalidade='Tudo ou Nada' and campanha_status in ('Sucesso', 'Aguardando Fundos','Falha') and autor_classificacao='Masculino'), 2)
		,round(100*count(1) filter (campanha_modalidade='Tudo ou Nada' and campanha_status in ('Sucesso', 'Aguardando Fundos') and autor_classificacao='Outros') / count(1) filter (campanha_modalidade='Tudo ou Nada' and campanha_status in ('Sucesso', 'Aguardando Fundos','Falha') and autor_classificacao='Outros'), 2)
		,round(100*count(1) filter (campanha_modalidade='Tudo ou Nada' and campanha_status in ('Sucesso', 'Aguardando Fundos') ) / count(1) filter (campanha_modalidade='Tudo ou Nada' and campanha_status in ('Sucesso', 'Aguardando Fundos','Falha') ), 2)
FROM	cte_campanhas
UNION ALL
SELECT	'taxa de sucesso: flex (%)' as 'variável'
		,round(100*count(1) filter (campanha_modalidade='Flex' and campanha_status in ('Sucesso', 'Aguardando Fundos') and autor_classificacao='Empresa') / count(1) filter (campanha_modalidade='Flex' and campanha_status in ('Sucesso', 'Aguardando Fundos','Falha') and autor_classificacao='Empresa'), 2)
		,round(100*count(1) filter (campanha_modalidade='Flex' and campanha_status in ('Sucesso', 'Aguardando Fundos') and autor_classificacao='Coletivo') / count(1) filter (campanha_modalidade='Flex' and campanha_status in ('Sucesso', 'Aguardando Fundos','Falha') and autor_classificacao='Coletivo'), 2)
		,round(100*count(1) filter (campanha_modalidade='Flex' and campanha_status in ('Sucesso', 'Aguardando Fundos') and autor_classificacao='Feminino') / count(1) filter (campanha_modalidade='Flex' and campanha_status in ('Sucesso', 'Aguardando Fundos','Falha') and autor_classificacao='Feminino'), 2)
		,round(100*count(1) filter (campanha_modalidade='Flex' and campanha_status in ('Sucesso', 'Aguardando Fundos') and autor_classificacao='Masculino') / count(1) filter (campanha_modalidade='Flex' and campanha_status in ('Sucesso', 'Aguardando Fundos','Falha') and autor_classificacao='Masculino'), 2)
		,round(100*count(1) filter (campanha_modalidade='Flex' and campanha_status in ('Sucesso', 'Aguardando Fundos') and autor_classificacao='Outros') / count(1) filter (campanha_modalidade='Flex' and campanha_status in ('Sucesso', 'Aguardando Fundos','Falha') and autor_classificacao='Outros'), 2)
		,round(100*count(1) filter (campanha_modalidade='Flex' and campanha_status in ('Sucesso', 'Aguardando Fundos') ) / count(1) filter (campanha_modalidade='Flex' and campanha_status in ('Sucesso', 'Aguardando Fundos','Falha') ), 2)
FROM	cte_campanhas
UNION ALL
SELECT	'arrecadação (por campanha)'
		,round(sum(geral_arrecadado_corrigido) filter (campanha_modalidade in ('Tudo ou Nada', 'Flex') and autor_classificacao='Empresa' and campanha_status in ('Sucesso', 'Aguardando Fundos')), 2)
		,round(sum(geral_arrecadado_corrigido) filter (campanha_modalidade in ('Tudo ou Nada', 'Flex') and autor_classificacao='Coletivo' and campanha_status in ('Sucesso', 'Aguardando Fundos')), 2)
		,round(sum(geral_arrecadado_corrigido) filter (campanha_modalidade in ('Tudo ou Nada', 'Flex') and autor_classificacao='Feminino' and campanha_status in ('Sucesso', 'Aguardando Fundos')), 2)
		,round(sum(geral_arrecadado_corrigido) filter (campanha_modalidade in ('Tudo ou Nada', 'Flex') and autor_classificacao='Masculino' and campanha_status in ('Sucesso', 'Aguardando Fundos')), 2)
		,round(sum(geral_arrecadado_corrigido) filter (campanha_modalidade in ('Tudo ou Nada', 'Flex') and autor_classificacao='Outros' and campanha_status in ('Sucesso', 'Aguardando Fundos')), 2)
		,round(sum(geral_arrecadado_corrigido) filter (campanha_modalidade in ('Tudo ou Nada', 'Flex')  and campanha_status in ('Sucesso', 'Aguardando Fundos')), 2)
FROM	cte_campanhas
UNION ALL
SELECT	'arrecadação: tudo ou nada (por campanha)'
		,round(sum(geral_arrecadado_corrigido) filter (campanha_modalidade='Tudo ou Nada' and autor_classificacao='Empresa' and campanha_status in ('Sucesso', 'Aguardando Fundos')), 2)
		,round(sum(geral_arrecadado_corrigido) filter (campanha_modalidade='Tudo ou Nada' and autor_classificacao='Coletivo' and campanha_status in ('Sucesso', 'Aguardando Fundos')), 2)
		,round(sum(geral_arrecadado_corrigido) filter (campanha_modalidade='Tudo ou Nada' and autor_classificacao='Feminino' and campanha_status in ('Sucesso', 'Aguardando Fundos')), 2)
		,round(sum(geral_arrecadado_corrigido) filter (campanha_modalidade='Tudo ou Nada' and autor_classificacao='Masculino' and campanha_status in ('Sucesso', 'Aguardando Fundos')), 2)
		,round(sum(geral_arrecadado_corrigido) filter (campanha_modalidade='Tudo ou Nada' and autor_classificacao='Outros' and campanha_status in ('Sucesso', 'Aguardando Fundos')), 2)
		,round(sum(geral_arrecadado_corrigido) filter (campanha_modalidade='Tudo ou Nada' and campanha_status in ('Sucesso', 'Aguardando Fundos')), 2)
FROM	cte_campanhas
UNION ALL
SELECT	'arrecadação: flex (por campanha)'
		,round(sum(geral_arrecadado_corrigido) filter (campanha_modalidade='Flex' and autor_classificacao='Empresa' and campanha_status in ('Sucesso', 'Aguardando Fundos')), 2)
		,round(sum(geral_arrecadado_corrigido) filter (campanha_modalidade='Flex' and autor_classificacao='Coletivo' and campanha_status in ('Sucesso', 'Aguardando Fundos')), 2)
		,round(sum(geral_arrecadado_corrigido) filter (campanha_modalidade='Flex' and autor_classificacao='Feminino' and campanha_status in ('Sucesso', 'Aguardando Fundos')), 2)
		,round(sum(geral_arrecadado_corrigido) filter (campanha_modalidade='Flex' and autor_classificacao='Masculino' and campanha_status in ('Sucesso', 'Aguardando Fundos')), 2)
		,round(sum(geral_arrecadado_corrigido) filter (campanha_modalidade='Flex' and autor_classificacao='Outros' and campanha_status in ('Sucesso', 'Aguardando Fundos')), 2)
		,round(sum(geral_arrecadado_corrigido) filter (campanha_modalidade='Flex' and campanha_status in ('Sucesso', 'Aguardando Fundos')), 2)
FROM	cte_campanhas
UNION ALL
SELECT	'arrecadação: recorrente (por mês)'
		,round(sum(geral_arrecadado_corrigido) filter (campanha_modalidade='Recorrente' and autor_classificacao='Empresa' and campanha_status in ('Sucesso', 'Aguardando Fundos', 'Publicado')), 2)
		,round(sum(geral_arrecadado_corrigido) filter (campanha_modalidade='Recorrente' and autor_classificacao='Coletivo' and campanha_status in ('Sucesso', 'Aguardando Fundos', 'Publicado')), 2)
		,round(sum(geral_arrecadado_corrigido) filter (campanha_modalidade='Recorrente' and autor_classificacao='Feminino' and campanha_status in ('Sucesso', 'Aguardando Fundos', 'Publicado')), 2)
		,round(sum(geral_arrecadado_corrigido) filter (campanha_modalidade='Recorrente' and autor_classificacao='Masculino' and campanha_status in ('Sucesso', 'Aguardando Fundos', 'Publicado')), 2)
		,round(sum(geral_arrecadado_corrigido) filter (campanha_modalidade='Recorrente' and autor_classificacao='Outros' and campanha_status in ('Sucesso', 'Aguardando Fundos', 'Publicado')), 2)
		,round(sum(geral_arrecadado_corrigido) filter (campanha_modalidade='Recorrente' and campanha_status in ('Sucesso', 'Aguardando Fundos', 'Publicado')), 2)
FROM	cte_campanhas


/*
variável	Catarse	Apoia.se	Todos
ano de início	2,011	2,016	2,011
campanhas	3,300	745	4,045
campanhas: tudo ou nada	1,479	0	1,479
campanhas: flex	1,750	12	1,762
campanhas: recorrente	71	733	804
movimentação (por campanha)	52,263,844.33	1,153.67	52,264,998
movimentação: tudo ou nada (por campanha)	29,551,287.87	[NULL]	29,551,287.87
movimentação: flex (por campanha)	22,712,556.46	1,153.67	22,713,710.13
movimentação: recorrente (por mês)	3,862.13	42,839.39	46,701.51
taxa de sucesso (%)	80.64	16.67	80.4
taxa de sucesso: tudo ou nada (%)	62.47	[NULL]	62.47
taxa de sucesso: flex (%)	95.2	16.67	94.67
arrecadação (por campanha)	50,517,963.11	1,138.45	50,519,101.56
arrecadação: tudo ou nada (por campanha)	27,805,556.58	[NULL]	27,805,556.58
arrecadação: flex (por campanha)	22,712,406.53	1,138.45	22,713,544.98
arrecadação: recorrente (por mês)	3,862.13	42,839.39	46,701.51
**/