select	m.municipio_id
		,m.nome			municipio
		,uf.acronimo	uf
		,uf.nome		uf_nome
from	Municipio m
join	UnidadeFederativa uf
on		uf.uf_id=m.uf_id
order	by 1
