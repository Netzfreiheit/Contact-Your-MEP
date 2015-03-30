CREATE TABLE IF NOT EXISTS faxes (
	id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY, 
	message text, 
	faxnr varchar(120), 
	create_date timestamp, 
	status int default 0, /* 0:new, 1:queed, 2:send, 3:retry, -1: error*/
	change_date timestamp, 
	campaign_id	INT UNSIGNED
);

CREATE TABLE IF NOT EXISTS subscriptions (
		id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY, 
		mail varchar(500), 
		country varchar(5), 
		create_date timestamp
);
