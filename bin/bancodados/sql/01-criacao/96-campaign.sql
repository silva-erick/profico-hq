CREATE TABLE IF NOT EXISTS campaign (
	campaign_id				INT,					--$.detail.project_id
	datasource_id			INT,
	name					VARCHAR(500),			--$.detail.name
	address_city			VARCHAR(500),			--$.detail.address.city
	address_state			VARCHAR(500),			--$.detail.address.state
	address_state_acronym	VARCHAR(500),			--$.detail.address.state_acronym
	user_id					INT,					--$.detail.user.id
	user_name				VARCHAR(500),			--$.detail.user.name
	user_public_name		VARCHAR(500),			--$.detail.user.public_name
	about_html				TEXT,					--$.detail.about_html
	about_txt				TEXT,
	is_about_clear			INT,					
	budget					TEXT,					--$.detail.budget
	admin_notes				TEXT,					--$.detail.admin_notes
	can_cancel				INT, 					--$.detail.can_cancel
	can_request_transfer	INT, 					--$.detail.can_request_transfer
	category_id				INT, 					--$.detail.category_id
	content_rating			INT, 					--$.detail.content_rating
	is_adult_content		INT,					--$.detail.is_adult_content
	contributed_by_friends	INT, 					--$.detail.contributed_by_friends
	elapsed_time_total		INT, 					--$.detail.elapsed_time.total
	elapsed_time_unit		VARCHAR(500), 			--$.detail.elapsed_time.unit
	expires_at				VARCHAR(500), 			--$.detail.expires_at
	goal					REAL,					--$.detail.goal
	in_reminder				INT, 					--$.detail.in_reminder
	is_published			INT, 					--$.detail.is_published
	mode					VARCHAR(500), 			--$.detail.mode
	online_date				VARCHAR(500), 			--$.detail.online_date
	online_days				INT, 					--$.detail.online_days
	permalink				VARCHAR(500), 			--$.detail.permalink
	pledged					REAL, 					--$.detail.pledged
	posts_count				INT, 					--$.detail.posts_count
	progress				REAL, 					--$.detail.progress
	recommended				INT, 					--$.detail.recommended
	service_fee				REAL, 					--$.detail.service_fee
	state					VARCHAR(500),			--$.detail.state
	tag_list				VARCHAR(500),			--$.detail.tag_list
	total_contributions		INT,					--$.detail.total_contributions
	total_contributors		INT, 					--$.detail.total_contributors
	total_posts				INT, 					--$.detail.total_posts
	video_url				VARCHAR(500),			--$.detail.video_url
	about_text				TEXT,
	original_json			TEXT,
	PRIMARY KEY (campaign_id, datasource_id)
);

CREATE INDEX IF NOT EXISTS idx_campaign_name ON campaign (
	name
);

CREATE INDEX IF NOT EXISTS idx_campaign_address ON campaign (
	address_city,
	address_state_acronym
);

CREATE INDEX IF NOT EXISTS idx_campaign_user ON campaign (
	user_id,
	user_name,
	user_public_name
);

CREATE INDEX IF NOT EXISTS idx_campaign_adultcontent ON campaign (
	is_adult_content
);

CREATE INDEX IF NOT EXISTS idx_campaign_mode ON campaign (
	mode
);

CREATE INDEX IF NOT EXISTS idx_campaign_state ON campaign (
	state
);

CREATE INDEX IF NOT EXISTS idx_campaign_onlinedate ON campaign (
	online_date
);
