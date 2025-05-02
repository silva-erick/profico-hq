INSERT 	INTO Municipio (municipio_id, nome, uf_id)
SELECT 	id, name, state_id
FROM	read_json('$(cities.json)') a
EXCEPT
SELECT 	municipio_id, nome, uf_id
FROM	Municipio 
;
