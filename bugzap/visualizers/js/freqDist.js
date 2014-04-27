var freq_dist_json; 

/*
Get the local json file to store into cached mem.
*/
function load_dataset(dataset, freqDist) {
	var path = 'data/' + dataset + '/' + freqDist + '.json';
    console.log('Loading dataset: ' + dataset);
    console.log(path)
    $.getJSON(path,
    	function(data) {
        freq_dist_json=data;
        console.log(freq_dist_json);
        graph_freq_dist(freq_dist_json);
    });
}

function graph_freq_dist(jdata) {
	var data = jdata;
	console.log('Preparing histogram');
	if (jdata != null) {
		var keys = $.map(data, function(value, key) {
			return key;
		})
		
		var values = $.map(data, function(value, key) {
			return value;
		});

		var container = $("#chart_container");

		var scale = d3.scale.linear()
		    .domain([0, d3.max(values)])
		    .range([0, (container.innerWidth() / d3.max(values)) - 4]);

		var chart = d3.select("#histogram");
		var bars = chart.selectAll("div");
		var barsUpdate = bars.data(Object.keys(data));
		var barsEnter = barsUpdate.enter().append("div");
		barsEnter.style("width", function(word) { return data[word] * scale(data[word]) + "px"; });
		barsEnter.style("height", function(word) { return 10 + "px"; });
		barsEnter.text(function(word) {return word;})
	} else {
		console.log('data cannot be found');
	}
}

/*
Call functions to load data and prepare bargraph.
*/
$(document).ready(function() {
	console.log('Document ready.');
});