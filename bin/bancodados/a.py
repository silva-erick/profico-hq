INSERT INTO Campanha (\n
 campanha_id\n
 ,origemdados_id\n
 ,original_id\n
 ,recompensas_menor_nominal\n
 ,recompensas_menor_ajustado\n
 ,recompensas_quantidade\n
 ,autor_id\n
 ,social_seguidores\n
 ,social_newsletter\n
 ,social_sub_contribuicoes_amigos\n
 ,social_sub_novos_seguidores\n
 ,social_sub_posts_projeto\n
 ,social_projetos_contribuidos\n
 ,social_projetos_publicados\n
 ,municipio_id\n
 ,geral_content_rating\n
 ,geral_contributed_by_friends\n
 ,geral_capa_imagem\n
 ,geral_capa_video\n
 ,geral_dias_campanha\n
 ,geral_data_fim\n
 ,geral_data_ini\n
 ,geral_meta\n
 ,geral_meta_corrigida\n
 ,geral_arrecadado\n
 ,geral_arrecadado_corrigido\n
 ,geral_percentual_arrecadado\n
 ,geral_conteudo_adulto\n
 ,geral_posts\n
 ,modalidadecampanha_id\n
 ,geral_titulo\n
 ,statuscampanha_id\n
 ,geral_total_contribuicoes\n
 ,geral_total_apoiadores\n
 ,geral_sobre\n)\nSELECT  nextval('seq_campanha_id')\n
 ,3\n
 ,'64136dd28d3b2d2731f44156'\n
 ,20.0\n
 ,21.571007134587312\n
 ,3\n    ,(SELECT autor_id FROM Autor WHERE original_id='9e6da4af-882b-40f9-b593-7c65dfc9ba77' AND origemdados_id=3)\n    ,0\n    ,False\n    ,0\n    ,0\n    ,0\n    ,0\n    ,0\n    ,4304\n
 ,\n\t,None\n\t,False\n\t,False\n\t,False\n\t,''\n\t,'2023-03-16T19:28:18.995'\n\t,5000\n\t,5000\n\t,0\n\t,0.0\n\t,0.0\n\t,False\n\t,0\n\t,3\n\t,'The MovieMakers'\n\t,3\n\t,0\n\t,0\n\t,'Olá! Sou Theo da Paz Herrmann, escritor e desenhista criador da webcomic The MovieMakers! Essa campanha foi feita para realizar a edição física do projeto, porque mesmo o meio digital ajudando e muito, ainda é sempre bom se manter no físico, não é? Hehe! Essa campanha é para todos que ainda não conhecem a comic, e para os que já a conhecem e gostariam de ter a coleção na sua prateleira.'\n\nWHERE   NOT EXISTS (\n    SELECT  1\n    FROM    Campanha\n    WHERE   origemdados_id=3\n    AND     original_id='64136dd28d3b2d2731f44156'\n)\n 