var resultsView = $('#resultsView')

function submitP2PForm (form) {
	alert('From: '+$('#p2pFrom').val()+' To: '+$('#p2pTo').val());
	return false;
}

// Set this up
function getResults () {
	sendAjaxRequest('url', function(data){
		replaceHTMLOfElement(resultsView, data);
		slideSearch(true);
	})
}

// Animate box on and off the screen
function slideSearch (offScreen) {
	var searchDiv = $('#p2pInputContainer')
	var speed = 350

	if (offScreen) {
		$('#contentDiv').addClass('noOverflow')
		resultsView.removeClass('hidden')
	    searchDiv.animate({
	        left: '-50%'
	    }, speed, "swing", function() {
	        searchDiv.addClass('hidden');
	    });

	    resultsView.animate({
	        left: '50%'
	    }, speed, "swing", function(){
	    	$('#contentDiv').removeClass('noOverflow');
	    });

	}else{
		$('#contentDiv').addClass('noOverflow')
		searchDiv.removeClass('hidden')
	    resultsView.animate({
	        left: '150%'
	    }, speed, "swing", function() {
	        resultsView.addClass('hidden');
	    });

	    searchDiv.animate({
	        left: '50%'
	    }, speed, "swing", function(){
	    	$('#contentDiv').removeClass('noOverflow');
	    });
	}
}

function getUrlParams() {
	var questionMarkIndex = window.location.href.indexOf('?');
	var result = {};
		if (questionMarkIndex !== -1) {
			var query = window.location.href.substring(questionMarkIndex+1);
			query.split("&").forEach(function(part) {
				var item = part.split("=");
				result[item[0]] = decodeURIComponent(item[1]);
			});
		};
		return result;
}

function objLength (obj){    
    var key,len=0;
    for(key in obj){
        len += Number( obj.hasOwnProperty(key) );
    }
    return len;
};

// Set this up
if (objLength(getUrlParams()) > 0) {
	getResults()
};
