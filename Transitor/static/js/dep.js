var resultsView = $('#resultsView')
var backButtonCode = "<a id=\"backButton\" href=\"javascript:slideSearch(false);\"></a>\n";

// Gets all the form's values and submits them. Also converts the values into the appropriate format
function submitDepBoardForm (form) {
	
	var station = returnValueIfExistsString($("input[name='depBoardFrom']"));
	var time = '';

	getResults(station, time);
	setPageTitle(station, time);
	return false;
}

// Helper function to ensure there is a value
function returnValueIfExistsString (element) {
	if (element.length && element.val()!="") {
		return element.val();
	}else{
		return '';
	}
}

// Create and send the Ajax request - customised which is why we don't use the ajax.js one
function sendDepTransitReq (params, callback) {
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
	  	// Success - display results
	  	callback(backButtonCode+xmlhttp.responseText);
	  }else if(xmlhttp.readyState==4){
	  	hideProgressBar();
	  	updateProgressBar(0);
	  	// There was an error - display an error message
	  	callback(backButtonCode+"<span style='display:block; text-align: center; color: white;'>There was an error. Please check your input and try again later.</span>");
	  }

	}

	// Build request
	xmlhttp.open("GET",'api/tb?'+params,true);

	// Show the loading bar
	showProgressBar();
	
	// Finally submit the request
	xmlhttp.send();
}


// creates the query string, sets the page URL and calls the ajax request
function getResults (station, time) {
	// Fix for hashes
	var queryString = 'station='+station+'&time='+time;
	updateHashWithoutTriggeringChange('pages/departureBoard/departureBoardInput.html?'+queryString);
	sendDepTransitReq(queryString, function(data){
		replaceHTMLOfElement(resultsView, data);
		resultsView.css('display', 'block');
		slideSearch(true);
	})
}

// Animate search form on and off the screen
function slideSearch (offScreen) {
	var searchDiv = $('#depBoardInputContainer')
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

// Parse url for params
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

// Function to count items in object
function objLength (obj){    
    var key,len=0;
    for(key in obj){
        len += Number( obj.hasOwnProperty(key) );
    }
    return len;
};


// Sets the page title
function setPageTitle (from, to) {
	var titleString = "Departure from: "+from;
	// var titleString = "Departure from: "+from+" at "+to;

	if ($('div.title.hidden').length) {
		$('div.title.hidden').html(titleString);
	}else{
		document.title = titleString;
	}
	
	console.log('Title string: '+titleString);
}


// Helper function to see if a parameter is empty. Returns true if not empty
function checkParamValues (param) {
	return !(param==''||param==undefined||param==null);
}

// These are executed on page load *****************************************

// If there are parameters, parse them into the form and request
if (objLength(getUrlParams()) > 0) {
	var params = getUrlParams();

	var station = params["station"];
	var time = params["time"];

// Fill form on page with old values
	if (checkParamValues(station)) {
		$("input[name='depBoardFrom']").val(station);
	};

	// if (checkParamValues(time)) {
	// 	$("input[name='p2ptime']").val(time);
	// };

	// TO BE REMOVED LATER!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
	time = '';

// Finally submit form
	getResults(station, time);
	setPageTitle(station, time);
};

// Autocomplete setup
$("input[name='depBoardFrom']").autocomplete({
	source: function (request, response) {
		$.get('http://transport.opendata.ch/v1/locations', {query:request.term}, function(data) {
			response($.map(data.stations, function(station) {
				return {
					label: station.name,
					station: station
				};
			}));
		}, 'json');
	},
	minLength: 2,
	select: function (event, ui) {
	}
});
