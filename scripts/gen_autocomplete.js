
/* 
	nodejs script to generate autocomplete client json
	@Author: Thomas Lohninger
	@Licence: CC0
*/

var data = require('../data/data.json');
var data_new = [];

for (var i = 0; i < data.length; i++) {
	try {
		
		data_new.push({'id': data[i].id, 'label': data[i].name, 'country': data[i].country_short, 'group': data[i].group_short});

	} catch (e) {
		console.error('couldn\'t update score of MEP # ' + i + ' because of ', e);
	}
}

//console.log(data_new); 

var fs = require('fs');
fs.writeFile("./data/data-autocomplete.json", JSON.stringify(data_new), function(err) {
		if(err) {
			console.log(err);
		}
});