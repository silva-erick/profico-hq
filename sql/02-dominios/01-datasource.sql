INSERT INTO datasource (
    datasource_id, title, is_crowdfunding_platform, url, description
)
SELECT  1, 'Guia dos Quadrinhos', 0, 'http://guiadosquadrinhos.com/', 'O maior banco de dados e acervo de capas de gibis publicados no Brasil. O objetivo principal é resgatar, preservar e divulgar a memória dos quadrinhos. Colecionadores e admiradores são bem-vindos a contribuir com novas informações, interagir com os outros usuários por meio de nossa rede social, e cadastrar suas coleções.'
WHERE   NOT EXISTS (
    SELECT 1 FROM datasource WHERE datasource_id=1
);

INSERT INTO datasource (
    datasource_id, title, is_crowdfunding_platform, url, description
)
SELECT  2, 'Catarse', 1, 'https://www.catarse.me/', 'Nascemos para incentivar a criatividade, a arte, o ativismo, a ciência e o empreendedorismo. Gostamos de projetos que trazem novas perspectivas, são disruptivos, geram diversidade e promovem debates saudáveis para a sociedade.'
WHERE   NOT EXISTS (
    SELECT 1 FROM datasource WHERE datasource_id=2
);
INSERT INTO datasource (
    datasource_id, title, is_crowdfunding_platform, url, description
)
SELECT  3, 'Apoia.se', 1, 'https://apoia.se/', 'Somos uma plataforma que viabiliza a sustentabilidade financeira de fazeres criativos e causas através do Financiamento Coletivo.'
WHERE   NOT EXISTS (
    SELECT 1 FROM datasource WHERE datasource_id=3
);
