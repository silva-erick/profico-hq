DROP TABLE IF EXISTS CampanhaHq;

CREATE TEMP TABLE IF NOT EXISTS CampanhaHq (
    campanha_origem                     VARCHAR(100)
    ,campanha_status                    VARCHAR(100)
    ,campanha_modalidade                VARCHAR(100)
    ,uf                                 VARCHAR(10)
    ,municipio                          VARCHAR(100)
    ,ano                                INT
    ,autor_classificacao                VARCHAR(100)
    ,autor_nome                         VARCHAR(100)
    ,autor_nome_publico                 VARCHAR(100)
	, campanha_id						INT
	,origemdados_id						INT
	,original_id						VARCHAR(100)	-- geral_project_id
	,recompensas_menor_nominal			DECIMAL(15, 3)
	,recompensas_menor_ajustado			DECIMAL(15, 3)
	,recompensas_quantidade				INT

	,autor_id							INT

	,social_seguidores					INT
	,social_newsletter					BIT
	,social_sub_contribuicoes_amigos	BIT
	,social_sub_novos_seguidores		BIT
	,social_sub_posts_projeto			BIT
	,social_projetos_contribuidos		INT
	,social_projetos_publicados			INT

	,municipio_id						INT

	,geral_content_rating				INT
	,geral_contributed_by_friends		BIT
	,geral_capa_imagem					BIT
	,geral_capa_video					BIT
	,geral_dias_campanha				INT
	,geral_data_fim						DATE
	,geral_data_ini						DATE
	,geral_meta							DECIMAL(15,3)
	,geral_meta_corrigida				DECIMAL(15,3)
	,geral_arrecadado					DECIMAL(15,3)
	,geral_arrecadado_corrigido			DECIMAL(15,3)
	,geral_percentual_arrecadado		DECIMAL(15,3)
	,geral_conteudo_adulto				BIT
	,geral_posts						INT

	,modalidadecampanha_id				INT

	,geral_titulo						VARCHAR(200)
	,statuscampanha_id					INT

	,geral_total_contribuicoes			INT
	,geral_total_apoiadores				INT

	,geral_sobre						TEXT

);

 WITH cte_campanhas as (
	SELECT	d.nome 			campanha_origem
			,sc.nome		campanha_status
			,mc.nome		campanha_modalidade
			,uf.acronimo	uf
			,m.nome			municipio
			,extract(year from geral_data_ini)	ano
			,ca.nome		autor_classificacao
			,a.nome			autor_nome
			,a.nome_publico	autor_nome_publico
			,c.*
	FROM	Campanha c
	JOIN	OrigemDados d
	ON		d.origemdados_id=c.origemdados_id
	JOIN	ModalidadeCampanha mc
	ON		mc.modalidadecampanha_id=c.modalidadecampanha_id
	JOIN	StatusCampanha sc
	ON 		sc.statuscampanha_id=c.statuscampanha_id
	JOIN	Autor a
	ON		a.autor_id=c.autor_id
	JOIN	ClassificacaoAutor ca
	ON		ca.classificacaoautor_id=a.classificacaoautor_id
	LEFT	JOIN	Municipio m
	ON		m.municipio_id=c.municipio_id
	LEFT	JOIN	UnidadeFederativa uf
	ON 		uf.uf_id=m.uf_id
)
INSERT  INTO    CampanhaHq
SELECT	*
FROM	cte_campanhas;

SELECT	*
FROM	CampanhaHq;

COPY CampanhaHq TO '/home/erick/Downloads/00-lista-campanhas.csv' WITH (
    FORMAT 'csv', 
    HEADER, 
    DELIMITER '|', 
    DATEFORMAT '%Y%m%d%H%M'
);
