INSERT INTO StatusCampanha (
    statuscampanha_id, nome
)
SELECT  *
FROM    (
    SELECT  1 statuscampanha_id, 'Sucesso' nome
    UNION ALL
    SELECT  2 , 'Falha'
    UNION ALL
    SELECT  3 , 'Publicado'
    UNION ALL
    SELECT  4 , 'Aguardando Fundos'
)
EXCEPT
SELECT  *
FROM    StatusCampanha
