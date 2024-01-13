CREATE TABLE IF NOT EXISTS user (
	user_id									INT,				-- $.user.id
	datasource_id							INT,
	name									VARCHAR(500),	    -- $.user.name
	public_name								VARCHAR(500),	    -- $.user.public_name
	newsletter								INT,	            -- $.user.newsletter
	facebook_link							VARCHAR(500),	    -- $.user.facebook_link
	twitter_username						VARCHAR(500),	    -- $.user.twitter_username
	created_at								VARCHAR(500),	    -- $.user.created_at
	mail_marketing_lists					VARCHAR(500),	    -- $.user.mail_marketing_lists
	total_contributed_projects				INT,	            -- $.user.total_contributed_projects
	total_published_projects				INT,	            -- $.user.total_published_projects
	subscribed_to_friends_contributions		INT,	            -- $.user.subscribed_to_friends_contributions
    original_json                           TEXT,
	PRIMARY KEY (user_id, datasource_id)
);