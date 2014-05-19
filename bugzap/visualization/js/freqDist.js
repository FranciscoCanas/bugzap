/**
 * Responsible for generating  SVG histograms out of a given 
 * json file that contains frequency distribution for any 
 * arbitrary set of objects or stats.
 */
var frequencyDistributionJson; 
/**
 * Get the local json file to store into cached mem.
 */
function loadDataset(dataset, freqDist, topNum) {
	var path = 'data/' + dataset + '/' + freqDist + '.json';
    console.log('Loading dataset: ' + dataset);
    $.getJSON(path,
    	function(data) {
        frequencyDistributionJson=data;
        graphFrequencyDistributionSvg(parseInt(topNum));
    });
    loadKeymap(dataset);
}

/**
 * Loads the given keymap from the given dataset.
 */
 function loadKeymap(dataset) {
 	var path = 'data/' + dataset + '/keymap.json';
 	console.log('Loading keymap for ' + dataset);
 	 $.getJSON(path,
    	function(data) {
        localStorage.setItem('_keyMapJson', JSON.stringify(data));
    });
 }

/**
 * Generates a frequency distribution chart out of a given
 * json of data using the svg library.
 *
 * @param {Int} Top number of items to chart.
 */
function graphFrequencyDistributionSvg(topNum) {
	if (frequencyDistributionJson != null) {
		var keys = Object.keys(frequencyDistributionJson);
		var values = $.map(frequencyDistributionJson, function(value, key) {
			return value;
		});
		
		graphData(topNum, keys, values);
		
	} else {
		console.log('data cannot be found');
	}
}

/**
 * Given a dataset, its keys, and its values, set up 
 * a chart, the graph and its axis, then fill the
 * graph with data.
 */
function graphData(topNum, keys, values) {
	var data = frequencyDistributionJson;
	var barHeight = 20;
	var xMax = d3.max(values);
	var lengths = $.map(keys, function(value, index) { return value.length; } );
	// make this based on longest label
	var xPadding = d3.max(lengths) * 8;
	var yPadding = 25;
    var width = $("body").width();
    var height = barHeight * Math.min(topNum, keys.length);
	

	// remove old sv.
	$("body svg").remove();
	
	// create chart svg container.
	var chart = d3.select("body").append("svg")
				.attr("class", "chart")
				.attr("id", "histogram")
				.attr("width", width)
    			.attr("height", height)
	
    // set up scales and x axis.
	var xScale = d3.scale.linear()
		.domain([0, xMax])
		.range([0, width - 2 * xPadding ]);

	var yScale = d3.scale.ordinal()
    	.domain(keys.slice(0,Math.min(topNum, keys.length) - 1))
    	.rangeBands([0,height]);

	var xAxis = d3.svg.axis()
	    .ticks(10)
	    .orient("top")
		.scale(xScale);

	var yAxis = d3.svg.axis()
		.orient("left")
		.scale(yScale);

	// draw chart lines.
	chart.selectAll("line.x")
		  .data(xScale.ticks(xMax))
		  .enter().append("line")
		  .attr("class", "x")
		  .attr("x1", xScale)
		  .attr("x2", xScale)
		  .attr("y1", 0)
		  .attr("y2", height)
		  .attr("transform", "translate(" + xPadding + "," + yPadding + ")")
		  .style("stroke", "#ccc");

    
    // fill graph with data.
	fillGraph(topNum, keys, values, chart, barHeight, xScale, xPadding, yPadding);

	// attach axis after filling graph.
	chart.append("g")
		.attr("class", "axis")
		.attr("id", "x-axis")
		.attr("transform", "translate(" + xPadding + "," + yPadding + ")")
		.call(xAxis);

	chart.append("g")
		.attr("class", "axis")
		.attr("id", "y-axis")
		.attr("transform", "translate(" + xPadding + "," + yPadding + ")")
		.call(yAxis);
}

/**
 * Given the dataset, a chart object, a bar height and 
 * an x scale functions, fill the graph. 
 */
function fillGraph(top, keys, values, chart, barHeight, xScale, xPadding, yPadding) {
	var data = frequencyDistributionJson;
	console.log(keys.slice(0,top));
	var bar = chart.selectAll("g")
			.data(keys.slice(0,top))
			.enter()
			.append("g")
			.attr("transform", function(item, index){
				return "translate(" + xPadding + "," + ((index * barHeight) + yPadding) +")";
			});

		bar.append("rect")
			.attr("height", barHeight - 1)
			.attr("width", function(item) {
				return xScale(data[item]);
			})
			.on("click", function(item) {
				$(this).append(transitionToKeyMap(item));
			});
}

function transitionToKeyMap(key) {
    localStorage.setItem('_current_key', key);
	location.href = 'keyToId.html';
}

/**
 * On loading the document, call functions 
 * to load data and prepare bargraph.
 */
$(document).ready(function() {
	console.log('Document ready.');
});
