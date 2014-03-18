
/* 
	nodejs script to give numerical IDs to scpared MEPs
	@Author: Thomas Lohninger, EDRi 
	@Licence: CC0
*/


var data = require('./data.json');

for (var i = 0; i < data.length; i++) {
	try {
		if (!data[i].id || !isNaN(data[i].id)) {
			data[i].id = i;
		}
	} catch (e) {
		console.error('couldn\'t give id to MEP # ' + i + ' because of ', e);
	}
}

//console.log(data); 

var fs = require('fs');
fs.writeFile("data.json", JSON.stringify(data), function(err) {
    if(err) {
        console.log(err);
    } else {
        console.log("ids written. The file was saved!");
    }
});

