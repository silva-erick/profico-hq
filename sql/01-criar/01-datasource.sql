CREATE TABLE IF NOT EXISTS datasource (
	 datasource_id				INT	PRIMARY KEY
	,title						VARCHAR(100)
	,is_crowdfunding_platform	INT
	,url						VARCHAR(5000)
	,description				TEXT
);

CREATE INDEX IF NOT EXISTS idx_datasource_title ON datasource (
	title
);
