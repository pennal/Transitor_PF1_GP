var resultsView = $('#resultsView')
var backButtonCode = "<a id=\"backButton\" href=\"javascript:slideSearch(false);\"></a>\n";

// Gets all the form's values and submits them. Also converts the values into the appropriate format
function submitWeatherForm (form) {
	$( "input" ).blur();
	var location = returnValueIfExistsString($("input[name='weatherLocation']"));

	getResults(location);
	setPageTitle(location);
	return false;
}

// Helper function to ensure there is a value
function returnValueIfExistsString (element) {
	if (element.length && checkParamValues(element.val())) {
		return element.val();
	}else{
		return '';
	}
}

// Create and send the Ajax request - customised which is why we don't use the ajax.js one
function sendWeatherReq (params, callback) {
	var xmlhttp;
	if (window.XMLHttpRequest)
	  {// code for IE7+, Firefox, Chrome, Opera, Safari
	  xmlhttp=new XMLHttpRequest();
	  }
	else
	  {// code for IE6, IE5
	  xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
	  }

	// Has the request finished?
	xmlhttp.onreadystatechange=function(){
	  
	  if (xmlhttp.readyState==4 && xmlhttp.status==200) {
	  	hideProgressBar();
	  	// Success - display results
	  	callback(backButtonCode+xmlhttp.responseText);
	  }else if(xmlhttp.readyState==4){
	  	hideProgressBar();
	  	// There was an error - display an error message
	  	callback(backButtonCode+"<span style='display:block; text-align: center; color: white;'>There was an error. Please check your input and try again later.</span>");
	  }

	}

	// Build request
	// xmlhttp.open("GET",'api/weather?'+params,true); PUT THIS BACK LATERRRR!!!
	xmlhttp.open("GET",'pages/weather/weather.html?'+params,true);

	// Show the loading bar
	showProgressBar();
	
	// Finally submit the request
	xmlhttp.send();
}


// creates the query string, sets the page URL and calls the ajax request
function getResults (theLocation) {
	// Fix for hashes
	var queryString = 'location='+theLocation;
	updateHashWithoutTriggeringChange('pages/weather/weatherInput.html?'+queryString);
	sendWeatherReq(queryString, function(data){
		replaceHTMLOfElement(resultsView, data);
		resultsView.css('display', 'block');
		slideSearch(true);
	})
}

// Animate search form on and off the screen
function slideSearch (offScreen) {
	var searchDiv = $('#weatherInputContainer')
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
	    	freezeArrows(false);
	    });

	}else{
		$('#contentDiv').addClass('noOverflow')
		searchDiv.removeClass('hidden')
	    resultsView.animate({
	        left: '150%'
	    }, speed, "swing", function() {
	        resultsView.addClass('hidden');
	    });

	    freezeArrows(true);

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
function setPageTitle (location) {
	var titleString = "Weather for: "+location;

	if ($('div.title.hidden').length) {
		$('div.title.hidden').html(titleString);
	}else{
		document.title = titleString;
	}
	
	console.log('Title string: '+titleString);
}


function freezeArrows (freeze) {
	var backButton = $('#backButton');

	var speed = 175;

	if (freeze) { //Animating results off screen
		backButton.animate({
			opacity: '0'
		}, { 
			duration: speed, queue: false, complete: function(){
				backButton.css({
					position: "absolute"
				});
			} 
		});

	}else{ //Animating results on screen

		backButton.animate({
			opacity: '1'
		}, { 
			duration: speed*2, queue: false 
		});
	};

}


// Helper function to see if a parameter is empty. Returns true if not empty
function checkParamValues (param) {
	return !(param==''||param==undefined||param==null);
}

// These are executed on page load *****************************************

// If there are parameters, parse them into the form and request
if (objLength(getUrlParams()) > 0) {
	var params = getUrlParams();

	var theLocation = params["location"];

// Fill form on page with old values
	if (checkParamValues(theLocation)) {
		$("input[name='weatherLocation']").val(theLocation);
	};

// Finally submit form
	getResults(theLocation);
	setPageTitle(theLocation);
};

// Autocomplete setup
$("input[name='weatherLocation']").autocomplete({
	source: function (request, response) {
		$.get('http://transport.opendata.ch/v1/locations', {query:request.term, type:'address'}, function(data) {
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
