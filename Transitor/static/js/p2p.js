var resultsView = $('#resultsView')

function submitP2PForm (form) {
	// alert('From: '+$('#p2pFrom').val()+' To: '+$('#p2pTo').val());
	var from = returnValueIfExistsString($('#p2pFrom'));
	var to = returnValueIfExistsString($('#p2pTo'));
	var via = returnValueIfExistsString($('#p2pVia'));
	var date = returnValueIfExistsString($('#p2pDate'));
	var time = returnValueIfExistsString($('#p2pTime'));
	var isArrivalTime = returnValueIfExistsString($('#p2pIsArrivalTime'));
	var transportations = returnValueIfExistsString($('#p2pTransportations'));
	var limit = returnValueIfExistsString($('#p2pLimit'));
	var direct = returnValueIfExistsString($('#p2pDirect'));
	var sleeper = returnValueIfExistsString($('#p2pSleeper'));
	var couchette = returnValueIfExistsString($('#p2pCouchette'));
	var bike = returnValueIfExistsString($('#p2pBike'));

	getResults(from, to, via, date, time, isArrivalTime, transportations, limit, direct, sleeper, couchette, bike);
	setPageTitle(from, to);
	return false;
}

function returnValueIfExistsString (element) {
	if (element.length && element.val()!="") {
		return element.val();
	}else{
		return '';
	}
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
	  	callback("<a id=\"backButton\" href=\"javascript:slideSearch(false);\"></a>\n"+xmlhttp.responseText);
	  }else if(xmlhttp.readyState==4){
	  	hideProgressBar();
	  	updateProgressBar(0);
	  	callback("<a id=\"backButton\" href=\"javascript:slideSearch(false);\"></a>\n<span style='display:block; text-align: center; color: white;'>There was an error. Please check your input and try again later.</span>");
	  }

	}

	// Build request
	xmlhttp.open("GET",'api/p2p?'+params,true);

	// Show the loading bar
	showProgressBar();
	
	// Finally submit the request
	xmlhttp.send();
}


// Set this up
function getResults (from, to, via, date, time, isArrivalTime, transportations, limit, direct, sleeper, couchette, bike) {
	// Fix for hashes
	var queryString = 'from='+from+'&to='+to+'&via='+via+'&date='+date+'&time='+time+'&isArrivalTime='+isArrivalTime+'&transportations='+transportations+'&limit='+limit+'&direct='+direct+'&sleeper='+sleeper+'&couchette='+couchette+'&bike='+bike;
	// var queryString = 'from='+from+'&to='+to;
	updateHashWithoutTriggeringChange('pages/p2p/input.html?'+queryString);
	sendP2PTransitReq(queryString, function(data){
		replaceHTMLOfElement(resultsView, data);
		$("#resultsView .resultSlider").first().addClass('frontResult');
		resultsView.css('display', 'block');
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



$('#additionalOptionsLink').click(function(event) {
	event.preventDefault();
	toggleAdditionalOptions();
});

if (objLength(getUrlParams()) > 1) {
	var params = getUrlParams();

	var from = params["from"];
	var to = params["to"]
	var via = params["via"];
	var date = params["date"];
	var time = params["time"];
	var isArrivalTime = params["isArrivalTime"];
	var transportations = params["transportations"];
	var limit = params["limit"];
	var direct = params["direct"];
	var sleeper = params["sleeper"];
	var couchette = params["couchette"];
	var bike = params["bike"];

	$('#p2pFrom').val(from);
	$('#p2pTo').val(to);
	$('#p2pVia').val(via);
	$('#p2pDate').val(date);
	$('#p2pTime').val(time);
	$('#p2pIsArrivalTime').val(isArrivalTime);
	$('#p2pTransportations').val(transportations);
	$('#p2pLimit').val(limit);
	$('#p2pDirect').val(direct);
	$('#p2pSleeper').val(sleeper);
	$('#p2pCouchette').val(couchette);
	$('#p2pBike').val(bike);

	getResults(from, to, via, date, time, isArrivalTime, transportations, limit, direct, sleeper, couchette, bike);
	setPageTitle(from, to);
};
