
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

var data = require('../data/data.json');

for (var i = 0; i < data.length; i++) {
	try {
		if (data[i].group_short.indexOf('epp') !== -1) {
			data[i].score = 0.4;
		} else if (data[i].group_short.indexOf('aldeadle') !== -1) {
			data[i].score = 0.3;
		}
		else if (data[i].group_short.indexOf('greensefa') !== -1) {
			data[i].score = 0.15;
		}
		else if (data[i].group_short.indexOf('sd') !== -1) {
			data[i].score = 0.3;
		}
		else if (data[i].group_short.indexOf('guengl') !== -1) {
			data[i].score = 015;
		}
		else if (data[i].group_short.indexOf('efd') !== -1) {
			data[i].score = 0.35;
		}
		else if (data[i].group_short.indexOf('ni') !== -1) {
			data[i].score = 0.3;
		}
		else {
			data[i].score = 0.1;
		}

		if ((data[i]['Members']||[]).indexOf('ITRE') != -1) {
			data[i].score += 0.5;
		} else if ((data[i]['Members']||[]).indexOf('IMCO') != -1) {
			data[i].score += 0.4;
		} else if ((data[i]['Substitute']||[]).indexOf('ITRE') != -1) {
			data[i].score += 0.2;
		} else if ((data[i]['Substitute']||[]).indexOf('IMCO') != -1) {
			data[i].score += 0.15;
		}

		if (data[i].id == "28340") {
			data[i].score=0.9;
		} else if (data[i].id == "96710") {
			data[i].score=0.9;
		}
	} catch (e) {
		console.error('couldn\'t update score of MEP # ' + i + ' because of ', e);
	}
}

//console.log(data); 

var fs = require('fs');
fs.writeFile("./data/data.json", JSON.stringify(data), function(err) {
    if(err) {
        console.log(err);
    } else {
        console.log("Scores updated. The file was saved!");
    }
});

