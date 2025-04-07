CREATE TABLE IF NOT EXISTS Campanha (
	 campanha_id						INT	PRIMARY KEY
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

	,modalidade_int						INT

	,geral_titulo						VARCHAR(200)
	,statuscampanha_id					INT

	,geral_total_contribuicoes			INT
	,geral_total_apoiadores				INT

	,geral_sobre						TEXT

);