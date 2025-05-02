INSERT 	INTO HistoricoLancamentos (
             origemdados_id
            ,anomes
            ,ano
            ,mes
            ,total
)
SELECT 	     1
            ,ano || mes
            ,ano
            ,mes
            ,total
FROM	read_json('$(lancamentos.json)') a
EXCEPT
SELECT 	     1
            ,ano || mes
            ,ano
            ,mes
            ,total
FROM	HistoricoLancamentos
;
