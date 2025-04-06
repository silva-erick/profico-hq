CREATE TABLE IF NOT EXISTS reward (
	reward_id				INT				,	-- $.rewards.id
	datasource_id			INT				,
	campaign_id				INT				,	-- $.rewards.project_id
	title					VARCHAR(500)	,	-- $.rewards.title
	description				TEXT			,	-- $.rewards.description
	maximum_contributions	INT				,	-- $.rewards.maximum_contributions
	minimum_value			INT				,	-- $.rewards.minimum_value
	shipping_options		VARCHAR(500)	,	-- $.rewards.shipping_options
	original_json			TEXT			,
	PRIMARY KEY (reward_id, datasource_id)
);

CREATE INDEX IF NOT EXISTS idx_reward_campaign_id ON reward (
	campaign_id
);

CREATE INDEX IF NOT EXISTS idx_reward_minimum_value ON reward (
	minimum_value
);
