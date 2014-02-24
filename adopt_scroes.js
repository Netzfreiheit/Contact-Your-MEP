
/* 
	nodejs script to update scores(likely hood of random selection) of MEPs
	@Author: Thomas Lohninger
	@Licence: CC0
	current logic
		shadow + rapporteur 0.9
		greens 0.25
		epp 
			members 0.8
			substitutes 0.5
		rest
			members 0.7
			substitutes 0.4
*/


var data = require('./data.json');

for (var i = 0; i < data.length; i++) {
	try {
		if (data[i].name.indexOf('Trautmann') !== -1 || data[i].name.indexOf('Andersdotter') !== -1 ) {
			data[i].score = 0.0;
		} else if (data[i].role.indexOf('shadow') !== -1 || data[i].role.indexOf('rapporteur') !== -1 ) {
			data[i].score = 0.9;
		}
		else if (data[i].group_short.indexOf('epp') !== -1 || data[i].group_short.indexOf('aldeadle') !== -1) {
			if (data[i].name.toUpperCase().indexOf('JOHANSSON') !== -1 || data[i].name.toUpperCase().indexOf('ALABART') !== -1 || data[i].name.toUpperCase().indexOf('GUNNAR') !== -1 || data[i].name.toUpperCase().indexOf('BELET') !== -1 || data[i].name.toUpperCase().indexOf('BUZEK') !== -1 || data[i].name.toUpperCase().indexOf('EHLER') !== -1 || data[i].name.toUpperCase().indexOf('KELLY') !== -1 || data[i].name.toUpperCase().indexOf('LANGEN') !== -1 || data[i].name.toUpperCase().indexOf('NIEBLER') !== -1 || data[i].name.toUpperCase().indexOf('NISTELROOIJ') !== -1 || data[i].name.toUpperCase().indexOf('RÜBIG') !== -1 || data[i].name.toUpperCase().indexOf('WINKLER') !== -1 || data[i].name.toUpperCase().indexOf('JORDAN') !== -1) {
				data[i].score = 0.8;
			} else if (data[i].role.indexOf('member') !== -1) {
				data[i].score = 0.6;
			} else {
				data[i].score = 0.5;
			}
		}
		else if (data[i].group_short.indexOf('greensefa') !== -1) {
			data[i].score = 0.1;
		}
		else if (data[i].group_short.indexOf('sd') !== -1) {
			data[i].score = 0.2;
		}
		else if (data[i].group_short.indexOf('guengl') !== -1) {
			data[i].score = 0.1;
		}
		else if (data[i].group_short.indexOf('efd') !== -1) {
			data[i].score = 0.0;
		}
		else {
			if (data[i].role.indexOf('member') !== -1) {
				data[i].score = 0.7;
			} else {
				data[i].score = 0.4;
			}
		}
	} catch (e) {
		console.error('couldn\'t update score of MEP # ' + i + ' because of ', e);
	}
}

//console.log(data); 

var fs = require('fs');
fs.writeFile("data.json", JSON.stringify(data), function(err) {
    if(err) {
        console.log(err);
    } else {
        console.log("Scores updated. The file was saved!");
    }
});

