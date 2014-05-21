/**
 * Responsible for generating links to the original 
 * BZ reports containing some given unigram. 
 */ 
var metaDataJson;
var keymap;
var bugmap;
var currentKey;
var currentDataset;
/**
 * Return the url to the given bz.
 */
function constructUrl(id) {
	var url = 'http://bugzilla.redhat.com/show_bug.cgi?id=' + id
	return url;
}

function getIdsFromKey(key) {
	return keymap[key];
}

function makeMap(keys) {
	var table = $('#mapToIdBody');
	$.each(keys, function(i,el) {
        	makeMapEntry(table, el);
    	});
}

/**
 * Loads the given keymap from the given dataset.
 */
 function loadKeymap(dataset) {
 	var path = ' data/' + dataset + '/keymap.json';
	console.log('Loading' + path); 	 
	$.getJSON(path,
    	function(data) {
        keymap = data;
        console.log(keymap);
        loadBugmap(dataset);
    });
 }

function loadBugmap(dataset) {
 	var path = ' data/' + dataset + '/bugmap.json';
 	console.log('Loading' + path);
 	 $.getJSON(path,
    	function(data) {
        bugmap = data;
        console.log(bugmap);
        makeMap(getIdsFromKey(currentKey));
    });	
 }

function makeMapEntry(parent, element) {
	var bug = bugmap[element];
	var desc = bug['description'];
	var keywords = bug['keywords'];

	parent.append('<tr><th><a href="'+ 
		constructUrl(element) + '">' + 
		element +'</a></th><td>' + 
		desc + '</td><td id="' + element + '"></td></tr>');

	var top5 = makeTopWords(keywords.slice(0,5));
	console.log(parent.find('#' + element).append(top5));	
}

function makeTopWords(keywords) {
	var top = $('<table class="inner"></table>');
	for (var word in keywords) {
 		top.append('<tr><td>' + keywords[word].join(": ") + '</td></tr>');
 		console.log(word +':'+ keywords[word]);
	}
	return top;
}

$(document).ready(function() {
	currentDataset = localStorage.getItem('_current_dataset');
	currentKey = localStorage.getItem('_current_key');
	$('#mapTitle').text(currentKey);
	loadKeymap(currentDataset);
});