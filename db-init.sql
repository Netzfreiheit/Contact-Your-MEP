DROP TABLE IF EXISTS faxes ;
CREATE TABLE faxes (
	id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY, 
	message text, 
	faxnr varchar(120), 
	create_date timestamp, 
	send_date timestamp, 
	send_attempts int, 
	send_rate int, 
	send_duration int, 
	status int default 0, /* 0:new, 1:in progress, 2:sended, -X: failed (x=attempts)*/
	send_reason varchar(500),
	send_pages int,
	send_jobtime time,
	send_conntime time,
	send_source_nr varchar(255)
	send_worker_id int /* ID of the worker, corresponds to virtual modem or SIPGATE account */
);