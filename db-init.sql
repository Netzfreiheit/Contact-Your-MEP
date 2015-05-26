CREATE TABLE IF NOT EXISTS faxes (
	id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY, 
	message text, 
	faxnr varchar(120), 
	status int default 0, /* 0:new, 1:queed, 2:send, 3:retry, -1: error, 5: stopped*/
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

CREATE TABLE IF NOT EXISTS meps (
	id INT UNSIGNED PRIMARY KEY, 
	name varchar(255),
	fax_bxl varchar(255),
	fax_stg varchar(255),
	country_short varchar(2),
	group_short varchar(12),
	fax_optout varchar(6)
);

#faxes/mep/day
select m.name, day(f.send_date), count(*) as cnt from faxes as f join meps as m on (m.fax_bxl=f.faxnr) WHERE f.id>=144 and f.faxnr not in ('003222849473', '0033388179473', '003222849732', '0033388179732', '0033388179681', '003222849681') group by 1,2 order by 1,2;

#avg nr of faxes /mep/day
select avg(cnt) from 
(select m.name, day(f.send_date), count(*) as cnt from faxes as f join meps as m on (m.fax_bxl=f.faxnr) WHERE f.id>=144 and f.faxnr not in ('003222849473', '0033388179473', '003222849732', '0033388179732', '0033388179681', '003222849681') group by 1,2 order by 1,2
	) as x;