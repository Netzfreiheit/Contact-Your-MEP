
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

Array.prototype.contains = function (el) {
	for (var i = 0; i < this.length; i++) {
		if (this[i] == el) {
			return true;
		}
	}
	return false;
}

var data = require('../data/data.json');
var execmd = require('child_process').exec;

for (var i = 0; i < data.length; i++) {
	try {
		if (data[i].group_short.indexOf('epp') !== -1) {
			data[i].score = 0.1;
		} else if (data[i].group_short.indexOf('aldeadle') !== -1) {
			data[i].score = 0.5;
		}
		else if (data[i].group_short.indexOf('greensefa') !== -1) {
			data[i].score = 0;
		}
		else if (data[i].group_short.indexOf('sd') !== -1) {
			data[i].score = 0.9;
		}
		else if (data[i].group_short.indexOf('guengl') !== -1) {
			data[i].score = 0.1;
		}
		else if (data[i].group_short.indexOf('efd') !== -1) {
			data[i].score = 0.7;
		}
		else if (data[i].group_short.indexOf('ecr') !== -1) {
			data[i].score = 0;
		}
		else if (data[i].group_short.indexOf('ni') !== -1) {
			data[i].score = 0.3;
		}
		else {
			data[i].score = 0.5;
		}


		/*
		if ((data[i]['Member']||[]).indexOf('ITRE') != -1 || (data[i]['Chair']||[]).indexOf('ITRE') != -1 || (data[i]['Vice-Chair']||[]).indexOf('ITRE') != -1) {
			data[i].score += 0.5;
		} else if ((data[i]['Member']||[]).indexOf('IMCO') != -1) {
			data[i].score += 0.4;
		} else if ((data[i]['Substitute']||[]).indexOf('ITRE') != -1) {
			data[i].score += 0.2;
		} else if ((data[i]['Substitute']||[]).indexOf('IMCO') != -1) {
			data[i].score += 0.15;
		}
		*/

		/*
		// shadows
		if (data[i].id == "28340") {
			data[i].score=0.9;
		} else if (data[i].id == "96710") {
			data[i].score=0.9;
		} else if (data[i].id == "96820") {
			data[i].score=0.9;
		} else if (data[i].id == "96949") {
			data[i].score=0.9;
		} else if (data[i].id == "124813") {
			data[i].score=0.9;
		}
		*/
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
			execmd("cat ./data/data.json | python -m json.tool > ./data/data.json.new && mv ./data/data.json.new ./data/data.json", function (error, stdout, stderr) {
				if (!error) {
					console.log("Scores updated. The file was saved!");
				}
			});
		}
});

