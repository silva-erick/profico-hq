INSERT INTO OrigemDados (
    origemdados_id, nome, is_plataforma_crowdfunding, url, descricao
)
SELECT  *
FROM    (
    SELECT  1 origemdados_id, 'Guia dos Quadrinhos' nome, 0 is_plataforma_crowdfunding, 'http://guiadosquadrinhos.com/' url, 'O maior banco de dados e acervo de capas de gibis publicados no Brasil. O objetivo principal é resgatar, preservar e divulgar a memória dos quadrinhos. Colecionadores e admiradores são bem-vindos a contribuir com novas informações, interagir com os outros usuários por meio de nossa rede social, e cadastrar suas coleções.' descricao
    UNION ALL
    SELECT  2, 'Catarse', 1, 'https://www.catarse.me/', 'Nascemos para incentivar a criatividade, a arte, o ativismo, a ciência e o empreendedorismo. Gostamos de projetos que trazem novas perspectivas, são disruptivos, geram diversidade e promovem debates saudáveis para a sociedade.'
    UNION ALL
    SELECT  3, 'Apoia.se', 1, 'https://apoia.se/', 'Somos uma plataforma que viabiliza a sustentabilidade financeira de fazeres criativos e causas através do Financiamento Coletivo.'
)
EXCEPT
SELECT  *
FROM    OrigemDados
