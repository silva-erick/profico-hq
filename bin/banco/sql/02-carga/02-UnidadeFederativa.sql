INSERT  INTO UnidadeFederativa (uf_id, acronimo, nome)
SELECT 	DISTINCT state_id, acronym, state_name
FROM	read_json('/home/erick/repos/profico-hq/dados/brutos/catarse/cities.json')
EXCEPT 
SELECT 	uf_id, acronimo, nome
FROM	UnidadeFederativa
;
