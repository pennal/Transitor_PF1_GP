var resultsView = $('#resultsView')

function submitP2PForm (form) {
	alert('From: '+$('#p2pFrom').val()+' To: '+$('#p2pTo').val());
	return false;
}

function getResults () {
	sendAjaxRequest('url', function(data){
		replaceHTMLOfElement(resultsView, data);
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