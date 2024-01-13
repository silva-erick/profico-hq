CREATE TABLE IF NOT EXISTS city (
	 city_id		INT	PRIMARY KEY
	,name			VARCHAR(100)
	,uf_id			INT
	,search			VARCHAR(200)
);

CREATE INDEX IF NOT EXISTS idx_city_search ON city (
	search
);
