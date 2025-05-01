select	a.autor_id
		,od.nome	plataforma
		,a.original_id
		,a.nome
		,a.nome_publico
		,ca.nome	classificacao_autoria
from	Autor a
join	OrigemDados od
on		od.origemdados_id=a.origemdados_id
join	ClassificacaoAutor ca
on		ca.classificacaoautor_id=a.classificacaoautor_id
order	by 1
