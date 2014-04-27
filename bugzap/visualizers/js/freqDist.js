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
        svg_graph_freq_dist(freq_dist_json);
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
			return Number(value);
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
		barsEnter.text(function(word) {return word;});
	} else {
		console.log('data cannot be found');
	}
}

function svg_graph_freq_dist(jdata) {
	var data = jdata;
	if (data != null) {
		var keys = Object.keys(data);
		var values = $.map(data, function(value, key) {
			return value;
		});
		console.log('dataset: ');
		console.log(data);
		console.log('values: ' + values);
		console.log('max: ' + d3.max(values));
		console.log('min: ' + d3.min(values));

		var width = 400;
		var barHeight = 20;

		var x = d3.scale.linear()
			.domain([1, d3.max(values)])
			.range([1, width]);

		// var xAxis = d3.svg.axis()
  //   		.scale(x)
  //   		.orient("top");

		console.log('number of entries: ' + keys.length);
		var chart = d3.select("#histogram")
			.attr("width", width)
			.attr("height", barHeight * keys.length);

		// chart.append("g")
  //   		.attr("class", "x axis")
  //   		.attr("transform", "translate(0,0)")
  //   		.call(xAxis);

		var bar = chart.selectAll("g")
			.data(Object.keys(data))
			.enter()
			.append("g")
			.attr("transform", function(item, index){
				return "translate(0," + index * barHeight +")";
			});

		bar.append("rect")
			.attr("height", barHeight - 1)
			.attr("width", function(item) {
				return x(data[item]);
			});

		bar.append("text")
			.attr("x", function(item) { 
				var pos = x(data[item]);
				return pos - 3;
			})
			.attr("y", barHeight / 2)
			.attr("dy", ".35em")
			.text(function(item){ return item; });
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