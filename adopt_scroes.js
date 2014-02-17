
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

var nlen = 0;
for (var i = 0; i < data.length; i++) {
	console.log(i, data[i].name, data[i].name.length);
	nlen = Math.max(data[i].name.length, nlen);
}
console.log(nlen);