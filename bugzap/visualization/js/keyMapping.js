/**
 * Responsible for generating links to the original 
 * BZ reports containing some given unigram. 
 */ 

 var metaDataJson;
 var keyMapJson;

/**
 * Loads the given file from the given dataset into
 * the specified container.
 */
 function loadJson(dataset, jfile, container) {
 	var path = 'data/' + dataset + '/' + jfile;
 	console.log('Loading ' + jfile + ' for ' + dataset);
 	 $.getJSON(path,
    	function(data) {
        container=eval(data);
    });
 }

 function loadKeymap(dataset) {
 	loadJson(dataset, 'keymap.json', keyMapJson);
 }

 function loadMetaData(dataset) {
 	loadJson(dataset, 'metadata.json', metaDataJson);
 }

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