var resultsView = $('#resultsView')

function submitP2PForm (form) {
	// alert('From: '+$('#p2pFrom').val()+' To: '+$('#p2pTo').val());
	var from = $('#p2pFrom').val();
	var to = $('#p2pTo').val();
	getResults(from, to);
	setPageTitle(from, to);
	return false;
}


function sendP2PTransitReq (params, callback) {
	var xmlhttp;
	if (window.XMLHttpRequest)
	  {// code for IE7+, Firefox, Chrome, Opera, Safari
	  xmlhttp=new XMLHttpRequest();
	  }
	else
	  {// code for IE6, IE5
	  xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
	  }

	  // Update the progress bar
	xmlhttp.onprogress = function(e){
	    if (e.lengthComputable){
	    	var progress = (e.loaded / e.total) * 100;
	        updateProgressBar(progress);
	    }
	};

	// Has the request finished?
	xmlhttp.onreadystatechange=function(){
	  
	  if (xmlhttp.readyState==4 && (xmlhttp.status==200||xmlhttp.status==0)) { //The 0 is just because it seemed to not like it when run locally..
	  	hideProgressBar();
	  	updateProgressBar(0);
	  	callback(xmlhttp.responseText);
	  }else{
	  }

	}

	// Build request
	xmlhttp.open("GET",'pointToPoint/doRequest?'+params,true);

	// Show the loading bar
	showLoadingAjax();
	
	// Finally submit the request
	xmlhttp.send();
}


// Set this up
function getResults (from, to) {
	// Fix for hashes
	updateHashWithoutTriggeringChange('pages/p2p/input.html?from='+from+'&to='+to);
	sendP2PTransitReq('from='+from+'&to='+to, function(data){
		console.log(data);
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
	        left: '-150%'
	    }, speed, "swing", function() {
	        searchDiv.addClass('hidden');
	    });

	    resultsView.animate({
	        left: '25%'
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
	        left: '0%'
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

function setPageTitle (from, to) {
	var titleString = "Point-to-Point: "+from+" to "+to;

	if ($('div.title.hidden').length) {
		$('div.title.hidden').html(titleString);
	}else{
		document.title = titleString;
	}
	
	console.log('Title string: '+titleString);
}

// Set this up
if (objLength(getUrlParams()) > 1) {
	var params = getUrlParams();

	var from = params["from"];
	var to = params["to"]
	
	getResults();

	getResults(from, to);
	setPageTitle(from, to);
};
