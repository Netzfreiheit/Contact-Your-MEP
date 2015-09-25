
/* 
	nodejs script to update scores(likely hood of random selection) of MEPs
	@Author: Thomas Lohninger
	@Licence: CC0
*/

var data = require('../data/data-full_list.json');
var cmds = [];

for (var i = 0; i < data.length; i++) {
	try {
		cmds.push("INSERT INTO meps(id,name,fax_bxl,fax_stg,country_short,group_short,fax_optout) VALUE("
			+ data[i]['id'] + 
			',"' + data[i]['name'] + '"' +
			',"' + unify_nr(data[i]['fax_bxl']) + '"' +
			',"' + unify_nr(data[i]['fax_stg']) + '"' +
			',"' + data[i]['country_short'] + '"' +
			',"' + data[i]['group_short'] + '"' +
			',"' + (data[i]['fax_output']||'false') + '"' +
			");");
	} catch (e) {
		console.error('couldn\'t update score of MEP # ' + i + ' because of ', e);
	}
}

//console.log(data); 

var fs = require('fs');
fs.writeFile("./data/insert_cmds.txt", cmds.join('\n'), function(err) {
		if(err) {
				console.log(err);
		} else {
			
		}
});

function unify_nr(nr) {
	return (nr || '').replace('+','00');
}

