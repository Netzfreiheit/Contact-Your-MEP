
/* 
	nodejs script to reduce lists of MEPs
	@Author: Thomas Lohninger
	@Licence: CC0
*/

var data = require('../data/data-full_list.json');
var data_new = [];
var execmd = require('child_process').exec;

for (var i = 0; i < data.length; i++) {
	try {
		
		if ((data[i]['name']||'').match(/Castillo/i) != null || 
			(data[i]['name']||'').match(/Matias/i) != null || 
			(data[i]['name']||'').match(/Toia/i) != null || 
			(data[i]['name']||'').match(/Tamburrano/i) != null || 
			(data[i]['name']||'').match(/Rohde/i) != null || 
			(data[i]['name']||'').match(/Tamburrano/i) != null || 
			(data[i]['name']||'').match(/Ford/i) != null || 
			(data[i]['name']||'').match(/Kammerevert/i) != null || 
			(data[i]['name']||'').match(/Reimon/i) != null) {
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
					console.log("Limit MEPs to negotiators. The file was saved!");
				}
			});
		}
});

