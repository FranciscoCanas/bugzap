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
	var table = $('#mapToIdBody');
	$.each(keys, function(i,el) {
        	makeMapEntry(table, el);
    	});
}

function makeMapEntry(parent, element) {
	var desc = 'temporary for now';
	parent.append('<tr><th><a href="'+ 
		constructUrl(element)+ '">' + 
		element +'</a></th><td>' + 
		desc + '</td>' +
		'<td>somestuff</td></tr>'
		);
}

$(document).ready(function() {
	var key = localStorage.getItem('_current_key');
	keyMapJson = JSON.parse(localStorage.getItem('_keyMapJson'));
	$('#mapTitle').text(key);
	makeMap(getIdsFromKey(key));
});