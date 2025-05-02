INSERT INTO ModalidadeCampanha (
    modalidadecampanha_id, nome, codigo
)
SELECT  *
FROM    (
    SELECT  1 modalidadecampanha_id, 'Tudo ou Nada' nome, 'aon' codigo
    UNION ALL
    SELECT  2 , 'Flex', 'flex'
    UNION ALL
    SELECT  3 , 'Recorrente', 'sub'
)
EXCEPT
SELECT  *
FROM    ModalidadeCampanha
