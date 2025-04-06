CREATE TABLE IF NOT EXISTS OrigemDados (
	 origemdados_id				INT	PRIMARY KEY
	,nome						VARCHAR(100)
	,is_plataforma_crowdfunding	BIT
	,url						VARCHAR(5000)
	,descricao					TEXT
);

--CREATE INDEX IF NOT EXISTS idx_OrigemDados_nome ON OrigemDados (
--	nome
--);
