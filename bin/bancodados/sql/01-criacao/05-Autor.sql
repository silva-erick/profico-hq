CREATE TABLE IF NOT EXISTS Autor (
	 autor_id				INT	PRIMARY KEY
	,origemdados_id			INT
	,original_id			VARCHAR(100)
	,nome					VARCHAR(200)
	,nome_publico			VARCHAR(200)
	,classificacaoautor_id	INT
);

CREATE SEQUENCE seq_autor_id START 1;