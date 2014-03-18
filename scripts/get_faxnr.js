
/* 
	nodejs script to give numerical IDs to scpared MEPs
	@Author: Thomas Lohninger, EDRi 
	@Licence: CC0
*/


var data = require('./../data/data.json');
var fs = require('fs');

var numbers = {
	'epp': (fs.readFileSync('./data/epp.csv') + '').split('\n')
	, 'sd': (fs.readFileSync('./data/sd.csv') + '').split('\n')
	, 'aldeadle': (fs.readFileSync('./data/alde.csv') + '').split('\n')
	, 'greensefa': (fs.readFileSync('./data/greens.csv') + '').split('\n')
	, 'guengl': (fs.readFileSync('./data/gue.csv') + '').split('\n')
	, 'ecr': (fs.readFileSync('./data/ecr.csv') + '').split('\n')
	, 'ni': (fs.readFileSync('./data/ni.csv') + '').split('\n')
	, 'efd': (fs.readFileSync('./data/efd.csv') + '').split('\n')
};

for (var i = 0; i < data.length; i++) {
	try {
		if (!data[i].fax || !data[i]['stg-fax']) {
			var line;
			for (var j = 0; j < numbers[data[i].group_short].length && !line; j++) {
				if (numbers[data[i].group_short][j].indexOf(data[i].email) != -1 || numbers[data[i].group_short][j].indexOf(data[i].name) != -1) {
					line = numbers[data[i].group_short][j];
				}
			}
			if (line && (line.split(',')[10] || line.split(',')[17])) {
				data[i].fax = line.split(',')[10]; 
				data[i]['stg-fax'] = line.split(',')[17];

				console.log(i, 'found fax ' + line.split(',')[10] + ' // ' + line.split(',')[17]);
			}
			else {
				console.log('no fax number for ' + i + ' ' + data[i] + ' ' + line);
			}
			line = undefined;
		}
	} catch (e) {
		console.error('couldn\'t give id to MEP # ' + i + data[i].group_short + ' because of ', e);
	}
}

//console.log(data); 

fs.writeFile("./data/data.json", JSON.stringify(data), function(err) {
    if(err) {
        console.log(err);
    } else {
        console.log("fax numbers written. The file was saved!");
    }
});

