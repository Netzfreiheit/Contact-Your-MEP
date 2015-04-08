CREATE TABLE IF NOT EXISTS faxes (
	id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY, 
	message text, 
	faxnr varchar(120), 
	status int default 0, /* 0:new, 1:queed, 2:send, 3:retry, -1: error*/
	create_date timestamp DEFAULT CURRENT_TIMESTAMP, 
	modify_date timestamp ON UPDATE CURRENT_TIMESTAMP, 
	send_date timestamp, 
	campaign_id	INT
);

CREATE TABLE IF NOT EXISTS subscriptions (
		id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY, 
		mail varchar(500), 
		country varchar(5), 
		create_date timestamp
);
