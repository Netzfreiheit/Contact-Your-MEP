DROP TABLE IF EXISTS faxes;
CREATE TABLE faxes (
	id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY, 
	message text, 
	faxnr varchar(120), 
	create_date timestamp, 
	status int default 0, /* 0:new, 1:queed, 2:send, 3:retry, -1: error*/
	change_date timestamp, 
	campaign_id	INT UNSIGNED
);