INSERT INTO ClassificacaoAutor (
    classificacaoautor_id, nome
)
SELECT  *
FROM    (
    SELECT  1 classificacaoautor_id, 'Empresa' nome
    UNION ALL
    SELECT  2 , 'Coletivo'
    UNION ALL
    SELECT  3 , 'Masculino'
    UNION ALL
    SELECT  4 , 'Feminino'
    UNION ALL
    SELECT  5 , 'Outros'
)
EXCEPT
SELECT  *
FROM    ClassificacaoAutor
