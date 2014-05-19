/**
 * Responsible for generating links to the original 
 * BZ reports containing some given unigram. 
 */ 
var metaDataJson;
var keyMapJson;
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
	var parent = $('#mapToId');
	$.each(keys, function(i,el) {
        	makeMapEntry(parent, el);
    	});
}

function makeMapEntry(parent, element) {
	parent.append('<div><a href="'+ constructUrl(element)+ '">' + element +'</a></div>');
}

$(document).ready(function() {
	var key = localStorage.getItem('_current_key');
	keyMapJson = JSON.parse(localStorage.getItem('_keyMapJson'));
	$('#mapTitle').text(key);
	makeMap(getIdsFromKey(key));
});