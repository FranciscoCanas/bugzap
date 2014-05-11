var frequencyDistributionJson; 

/**
 * Get the local json file to store into cached mem.
 */
function loadDataset(dataset, freqDist, topNum) {
	var path = 'data/' + dataset + '/' + freqDist + '.json';
    console.log('Loading dataset: ' + dataset);
    console.log(path)
    $.getJSON(path,
    	function(data) {
        frequencyDistributionJson=data;
        console.log(frequencyDistributionJson);
        graphFrequencyDistributionSvg(parseInt(topNum));
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
	var width = $("body").width();
	var xMax = d3.max(values);
	var barHeight = 20;

	// remove old sv.
	$("body svg").remove();
	
	// create chart svg container.
	var chart = d3.select("body").append("svg")
				.attr("class", "chart")
				.attr("id", "histogram")
				.attr("width", width)
				.attr("height", barHeight * (topNum + 1));

    // set up scales and x axis.
	var xScale = d3.scale.linear()
		.domain([0, xMax + 1])
		.range([0, width]);

	var yScale = d3.scale.linear()
		.range([0,barHeight * keys.length]);

	var xAxis = d3.svg.axis()
	    .ticks(xMax)
		.scale(xScale);

	// draw chart lines.
	chart.selectAll("line.x")
		  .data(xScale.ticks(xMax))
		  .enter().append("line")
		  .attr("class", "x")
		  .attr("x1", xScale)
		  .attr("x2", xScale)
		  .attr("y1", 0)
		  .attr("y2", barHeight * (topNum + 1))
		  .style("stroke", "#ccc");

    
    // fill graph with data.
	fillGraph(topNum, keys, values, chart, barHeight, xScale);

	// attach axis after filling graph.
	chart.append("g")
		.attr("class", "axis")
		.attr("id", "x-axis")
		.call(xAxis);
}

/**
 * Given the dataset, a chart object, a bar height and 
 * an x scale functions, fill the graph. 
 */
function fillGraph(top, keys, values, chart, barHeight, xScale) {
	var data = frequencyDistributionJson;
	console.log(keys.slice(0,top));
	var bar = chart.selectAll("g")
			.data(keys.slice(0,top))
			.enter()
			.append("g")
			.attr("transform", function(item, index){
				return "translate(0," + (index + 1)* barHeight +")";
			});

		bar.append("rect")
			.attr("height", barHeight - 1)
			.attr("width", function(item) {
				return xScale(data[item]);
			});

		bar.append("text")
			.attr("x", function(item) { 
				var pos = xScale(data[item]);
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