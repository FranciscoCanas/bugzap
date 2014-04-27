var keywords_json; 

/*
Get the local json file to store into cached mem.
*/
function load_dataset(dataset) {
	var path = 'data/' + dataset + '/keywords.json';
    console.log('Loading dataset: ' + dataset);
    console.log(path)
    $.getJSON(path,
    	function(data) {
        keywords_json=data;
        console.log(keywords_json);
        prepare_graph(keywords_json);
    });
}

/*
Takes a json full of processed bugs and extracts all
the individual bugs' keywords.
*/
function extract_keywords(data) {
	var keywords = [];
	data.forEach(function(bug) {
    	console.log(bug['keywords']);
    	keywords = keywords.concat(bug['keywords']);
	});
	return keywords;
}


function prepare_graph(jdata) {
	var data = jdata;
	console.log('Preparing bargraph');
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

		var chart = d3.select("#keywords");
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