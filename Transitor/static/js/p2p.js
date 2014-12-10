var resultsView = $('#resultsView')
var backButtonCode = "<a id=\"backButton\" href=\"javascript:slideSearch(false);\"></a>\n";

// Formats the date for the user and also for the API
function dateFormat (forURL, value) {
	if (forURL) {
		var date = '';
		if (value && value != '') {
			date = $.datepicker.formatDate('yy-mm-dd', value);
		};
		return date;
	}else{
		value = new Date(value);
		var date = '';
		if (value && value != '') {
			date = $.datepicker.formatDate('dd.mm.yy', value);
		};
		return date;
	}
}

// Gets all the form's values and submits them. Also converts the values into the appropriate format
function submitP2PForm (form) {
	var from = returnValueIfExistsString($("input[name='p2pFrom']"));
	var to = returnValueIfExistsString($("input[name='p2pTo']"));
	var via = returnValueIfExistsString($("input[name='p2pVia']"));
	
	var date = dateFormat(true, $("input[name='p2pDate']").datepicker("getDate"));
	
	var time = returnValueIfExistsString($("input[name='p2pTime']"));

	var isArrivalTime = returnValueIfExistsString($("input[name='p2pIsArrivalTime']:checked"));
	
	var checked = [];
	$("input[name='p2pTransportationType[]']:checked").each(function(){
	    checked.push($(this).val());
	});

	var transportations =  checked.toString();

 	var radioSelectionValue = $("input[name='p2pConnectionType']:checked").val();
	var direct = '0';
	var sleeper = '0';
	var couchette = '0';

	switch(radioSelectionValue){
		case '0':
			break;
		case '1':
			direct = '1';
			break;
		case '2':
			sleeper = '1';
			break;
		case '3':
			couchette = '1';
			break;
		default:
			break;
	}


	var bike = $("input[name='p2pBike']").prop("checked") > 0 ? '1' : '0';

	getResults(from, to, via, date, time, isArrivalTime, transportations, direct, sleeper, couchette, bike);
	setPageTitle(from, to);
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
	xmlhttp.open("GET",'api/p2p?'+params,true);

	// Show the loading bar
	showProgressBar();
	
	// Finally submit the request
	xmlhttp.send();
}


// creates the query string, sets the page URL and calls the ajax request
function getResults (from, to, via, date, time, isArrivalTime, transportations, direct, sleeper, couchette, bike) {
	// Fix for hashes
	var queryString = 'from='+from+'&to='+to+'&via='+via+'&date='+date+'&time='+time+'&isArrivalTime='+isArrivalTime+'&transportations='+transportations+'&direct='+direct+'&sleeper='+sleeper+'&couchette='+couchette+'&bike='+bike;
	// var queryString = 'from='+from+'&to='+to;
	updateHashWithoutTriggeringChange('pages/p2p/input.html?'+queryString);
	sendP2PTransitReq(queryString, function(data){
		replaceHTMLOfElement(resultsView, data);
		$("#resultsView .resultSlider").first().addClass('frontResult');
		resultsView.css('display', 'block');
		slideSearch(true);
	})
}

// Animate search form on and off the screen
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
	var titleString = "Point-to-Point: "+from+" to "+to;

	if ($('div.title.hidden').length) {
		$('div.title.hidden').html(titleString);
	}else{
		document.title = titleString;
	}
	
	console.log('Title string: '+titleString);
}

// Shows and hides additional options
function toggleAdditionalOptions () {
	var theBox = $("#additionalOptions");
	if (theBox.hasClass('closed')) {
		theBox.fadeIn(300, function(){
			theBox.removeClass('closed');
		});
		$('#additionalOptionsLink').html("-Fewer Options");
	}else{
		theBox.fadeOut(300, function(){
			theBox.addClass('closed');
		});
		$('#additionalOptionsLink').html("+Additional Options");
	};
}


// Function to animate the cards sliding out front to back
function slideOutFrontAndReplace () {
	var frontCard = $('.frontResult');
	var secondCard = frontCard.next();
	
	frontCard.animate({
       left: '-150%'
    }, { duration: 500, queue: false, complete: function(){
    	frontCard.removeClass('frontResult');
    	secondCard.addClass('frontResult');
    	frontCard.css('left', '');
    	frontCard.css('opacity', '0');
    	frontCard = frontCard.detach();
    	resultsView.append(frontCard);
    } });

    secondCard.animate({
       opacity: '1'
    }, { duration: 500, queue: false });
}


// Helper function to see if a parameter is empty. Returns true if not empty
function checkParamValues (param) {
	return !(param==''||param==undefined||param==null);
}

// These are executed on page load *****************************************

// Set up date Picker
$("input[name='p2pDate']").datepicker({
	dateFormat: "dd.mm.yy"
});

// Attach function to click event on additional options
$('#additionalOptionsLink').click(function(event) {
	event.preventDefault();
	toggleAdditionalOptions();
});

// If there are parameters, parse them into the form and request
if (objLength(getUrlParams()) > 1) {
	var params = getUrlParams();

	var from = params["from"];
	var to = params["to"]
	var via = params["via"];
	var date = params["date"];
	var time = params["time"];
	var isArrivalTime = params["isArrivalTime"];
	var transportations = params["transportations"];
	var direct = params["direct"];
	var sleeper = params["sleeper"];
	var couchette = params["couchette"];
	var bike = params["bike"];

// Fill form on page with old values
	if (checkParamValues(from)) {
		$("input[name='p2pFrom']").val(from);
	};
	if (checkParamValues(to)) {
		$("input[name='p2pTo']").val(to);
	};
		
	if (checkParamValues(via)) {
		$("input[name='p2pVia']").val(via);
	};
	
	if (checkParamValues(date)) {
		$("input[name='p2pDate']").val(dateFormat(false,date));
	};

	if (checkParamValues(time)) {
		$("input[name='p2pTime']").val(time);
	};
	
	if (checkParamValues(isArrivalTime)&&isArrivalTime=='1') {
		$("input[name='p2pIsArrivalTime'][value='0']").prop("checked", false);
		$("input[name='p2pIsArrivalTime'][value='1']").prop("checked", true);
	}else{
		$("input[name='p2pIsArrivalTime'][value='0']").prop("checked", true);
		$("input[name='p2pIsArrivalTime'][value='1']").prop("checked", false);
	}


	if (checkParamValues(transportations)) {
		var transpArray = transportations.split(",");
		$("input[name='p2pTransportationType[]']").each(function (){
			if (transpArray.indexOf($(this).val()) > -1) {
				$(this).prop("checked", true);
			}else{
				$(this).prop("checked", false);
			}
		});
	};


	if (direct == '1') {
		$("input[name='p2pConnectionType'][value='1']").prop("checked", true);
	}else if(sleeper == '1'){
		$("input[name='p2pConnectionType'][value='2']").prop("checked", true);
	}else if(couchette == '1'){
		$("input[name='p2pConnectionType'][value='3']").prop("checked", true);
	}else{
		$("input[name='p2pConnectionType'][value='0']").prop("checked", true);
	}

	if (checkParamValues(bike)) {
		if (bike =='1') {
			$("input[name='p2pBike']").prop("checked", true);
		}else{
			$("input[name='p2pBike']").prop("checked", false);
		}
	};

	
// Finally submit form
	getResults(from, to, via, date, time, isArrivalTime, transportations, direct, sleeper, couchette, bike);
	setPageTitle(from, to);
};
