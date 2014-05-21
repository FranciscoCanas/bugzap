/**
 * Responsible for generating links to the original 
 * BZ reports containing some given unigram. 
 */ 
var metaDataJson;
var keyMapJson;
var bugMapJson;
var chosenKey;
/**
 * Return the url to the given bz.
 */
function constructUrl(id) {
	var url = 'http://bugzilla.redhat.com/show_bug.cgi?id=' + id
	return url;
}

function getIdsFromKey(key) {
	return keyMapJson[key];
}

function makeMap(keys) {
	var table = $('#mapToIdBody');
	$.each(keys, function(i,el) {
        	makeMapEntry(table, el);
    	});
}

function makeMapEntry(parent, element) {
	var bug = bugMapJson[element];
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
	chosenKey = localStorage.getItem('_current_key');
	keyMapJson = JSON.parse(localStorage.getItem('_keyMapJson'));
	bugMapJson = JSON.parse(localStorage.getItem('_bugMapJson'));
	$('#mapTitle').text(chosenKey);
	makeMap(getIdsFromKey(chosenKey));
});