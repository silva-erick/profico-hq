SELECT      CASE
                WHEN    lower(u.name) LIKE '%editora%'
                OR      lower(public_name)  LIKE '%editora%'
                --OR      lower(u.name) LIKE '%studio%'
                --OR      lower(public_name)  LIKE '%studio%'
                --OR      lower(u.name) LIKE '%estúdio%'
                --OR      lower(public_name)  LIKE '%estúdio%'
                --OR      lower(u.name) LIKE '%quadrinhos%'
                --OR      lower(public_name)  LIKE '%quadrinhos%'
                --OR      lower(u.name) LIKE '%comics%'
                --OR      lower(public_name)  LIKE '%comics%'
                OR      lower(u.name) LIKE '%livros%'
                OR      lower(public_name)  LIKE '%livros%'
                OR      lower(u.name) LIKE '%gráfica%'
                OR      lower(public_name)  LIKE '%gráfica%'
                --OR      lower(u.name) LIKE '%entertainment%'
                --OR      lower(public_name)  LIKE '%entertainment%'
                --OR      lower(u.name) LIKE '%entretenimento%'
                --OR      lower(public_name)  LIKE '%entretenimento%'
                --OR      lower(u.name) LIKE '%ltda%'
                --OR      lower(public_name)  LIKE '%ltda%'
                --OR      lower(u.name) LIKE '% eireli%'
                --OR      lower(public_name)  LIKE '% eireli%'
                --OR      lower(public_name) IN ('ugra press','red dragon','indievisivel press')
                THEN 1
                ELSE 0
            END is_editora
            ,u.user_id
            ,u.name 'name'
            ,u.public_name
            ,COUNT(1)
FROM        user u
JOIN        campaign c
ON          c.user_id = u.user_id
--WHERE       name LIKE '%fica%' OR public_name LIKE '%fica%'
GROUP BY    u.user_id, u.name, u.public_name
ORDER BY    1, 5 DESC