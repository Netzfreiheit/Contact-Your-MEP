
/* 
	nodejs script to reduce lists of MEPs
	@Author: Thomas Lohninger
	@Licence: CC0
*/

var data = require('../data/data.json');
var data_new = [];
var execmd = require('child_process').exec;

for (var i = 0; i < data.length; i++) {
	try {
		
		if ((data[i]['Members']||[]).indexOf('ITRE') != -1 || 
			(data[i]['Members']||[]).indexOf('IMCO') != -1 || 
			(data[i]['Chair']||[]).indexOf('ITRE') != -1 || 
			(data[i]['Vice-Chair']||[]).indexOf('ITRE') != -1 || 
			(data[i]['Chair']||[]).indexOf('IMCO') != -1 || 
			(data[i]['Vice-Chair']||[]).indexOf('IMCO') != -1 || 
			(data[i]['Substitute']||[]).indexOf('ITRE') != -1 || 
			(data[i]['Substitute']||[]).indexOf('IMCO') != -1) {
			data_new.push(data[i]);
		}

	} catch (e) {
		console.error('couldn\'t update score of MEP # ' + i + ' because of ', e);
	}
}

//console.log(data); 

var fs = require('fs');
fs.writeFile("./data/data.json", JSON.stringify(data_new), function(err) {
		if(err) {
				console.log(err);
		} else {
			execmd("cat ./data/data.json | python -m json.tool > ./data/data.json.new && mv ./data/data.json.new ./data/data.json", function (error, stdout, stderr) {
				if (!error) {
					console.log("Limit MEPs to ITRE and IMCO. The file was saved!");
				}
			});
		}
});

