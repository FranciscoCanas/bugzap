var frequencyDistributionJson; 

/**
 * Get the local json file to store into cached mem.
 */
function loadDataset(dataset, freqDist) {
	var path = 'data/' + dataset + '/' + freqDist + '.json';
    console.log('Loading dataset: ' + dataset);
    console.log(path)
    $.getJSON(path,
    	function(data) {
        frequencyDistributionJson=data;
        console.log(frequencyDistributionJson);
        graphFrequencyDistributionSvg(frequencyDistributionJson);
    });
}

/**
 * Generates a frequency distribution chart out of a given
 * json of data using the svg library.
 *
 * @param {json} A json containing a frequency distribution.
 */
function graphFrequencyDistributionSvg(jdata) {
	var data = jdata;
	if (data != null) {
		var keys = Object.keys(data);
		var values = $.map(data, function(value, key) {
			return value;
		});
		
		graphData(data, keys, values);
		
	} else {
		console.log('data cannot be found');
	}
}

/**
 * Given a dataset, its keys, and its values, set up 
 * a container, the graph and its axis, then fill the
 * graph with data.
 */
function graphData(data, keys, values) {
		var container = $("#chart_container");

		var width = container.innerWidth();
		var barHeight = 20;

		var x_scale = d3.scale.linear()
			.domain([0, d3.max(values)])
			.range([0, width]);

		var y_scale = d3.scale.linear()
			.range([0,barHeight * keys.length]);

		var xAxis = d3.svg.axis()
    		.scale(x_scale)
    		.orient("top");

		var chart = d3.select("#histogram")
			.attr("width", width)
			.attr("height", barHeight * keys.length);

		chart.append("g")
    		.attr("class", "x axis")
    		.call(xAxis);

    	fillGraph(data, chart, barHeight, x_scale);
}

/**
 * Given the dataset, a chart object, a bar height and 
 * an x scale functions, fill the graph. 
 */
function fillGraph(data, chart, barHeight, x_scale) {
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
				return x_scale(data[item]);
			});

		bar.append("text")
			.attr("x", function(item) { 
				var pos = x_scale(data[item]);
				return pos - 3;
			})
			.attr("y", barHeight / 2)
			.attr("dy", ".35em")
			.text(function(item){ return item; });
}

/**
 * On loading the document, call functions 
 * to load data and prepare bargraph.
 */
$(document).ready(function() {
	console.log('Document ready.');
});