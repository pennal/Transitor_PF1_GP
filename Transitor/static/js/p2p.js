// Helpful variables;
var resultsView = $('#resultsView')
var cardNumCodeTextField = "Card %current% of %total%";
var currentCardNum = 1;
var totalCardNum = 1;
var isTransitioningCard = false;

// Additional code to add to results
var cardNumCode = "<div id=\"cardNumTag\"></div>";
var buttonDivCode = "<div id=\"buttonDiv\"><a id=\"backButton\" href=\"javascript:slideSearch(false);\"></a><a id=\"homeButtonAlternate\" class=\"internal\" href=\"pages/home.html\"></a></div>\n";
var navRightArrowCode = "<a href=\"javascript:slideOutFrontAndReplace();\" id=\"rightarrow\"></a>";
var navLeftArrowCode = "<a href=\"javascript:slideInBackAndReplace();\" id=\"leftarrow\"></a>";

var additionalCode = cardNumCode+buttonDivCode+navRightArrowCode+navLeftArrowCode;

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
	$( "input" ).blur();
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
	if (element.length && checkParamValues(element.val())) {
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

	// Has the request finished?
	xmlhttp.onreadystatechange=function(){
	  
	  if (xmlhttp.readyState==4 && xmlhttp.status==200) {
	  	hideProgressBar();
	  	// Success - display results
	  	callback(additionalCode+xmlhttp.responseText);
	  }else if(xmlhttp.readyState==4){
	  	hideProgressBar();
	  	// There was an error - display an error message
	  	callback(buttonDivCode+"<span style='display:block; text-align: center; color: white;'>There was an error. Please check your input and try again later.</span>");
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
		// Listens for clicks on cal button
		setUpClickOnCalButton();
		// Tooltip setup for calButton
		$(".calButton").tooltip();

		// Work out how many cards there are
		totalCardNum = $(".resultSlider").length;
		updateCardNumText();

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
	    }, {duration:speed, queue: false, complete:function(){
	        searchDiv.addClass('hidden');
	    }});

	    resultsView.animate({
	        left: '25%'
	    }, {duration:speed, queue: false, complete:function(){
	    	$('#contentDiv').removeClass('noOverflow');
	    	freezeArrows(false);
	    }});

	}else{
		$('#contentDiv').addClass('noOverflow')
		searchDiv.removeClass('hidden')
	    resultsView.animate({
	        left: '150%'
	    }, {duration:speed, queue: false, complete:function(){
	        resultsView.addClass('hidden');
	    }});

	    freezeArrows(true);

	    searchDiv.animate({
	        left: '0%'
	    }, {duration:speed, queue: false, complete:function(){
	    	$('#contentDiv').removeClass('noOverflow');
	    }});
	}
}

function freezeArrows (freeze) {
	var leftarrow = $('#leftarrow');
	var rightarrow = $('#rightarrow');
	var buttonDiv = $('#buttonDiv');

	var speed = 175;

	if (freeze) { //Animating results off screen
		
		leftarrow.animate({
			opacity: '0'
		}, { 
			duration: speed, queue: false, complete: function(){
				leftarrow.css({
					top: leftarrow.offset().top,
					position: "absolute"
				});
			} 
		});

		rightarrow.animate({
			opacity: '0'
		}, { 
			duration: speed, queue: false, complete: function(){
				rightarrow.css({
					top: rightarrow.offset().top,
					position: "absolute"
				});
			} 
		});

		buttonDiv.animate({
			opacity: '0'
		}, { 
			duration: speed, queue: false, complete: function(){
				buttonDiv.css({
					position: "absolute"
				});
			} 
		});

		$("body").off("keydown", handleKeyPress);

	}else{ //Animating results on screen
		leftarrow.animate({
			opacity: '1'
		}, { 
			duration: speed*2, queue: false 
		});

		rightarrow.animate({
			opacity: '1'
		}, { 
			duration: speed*2, queue: false 
		});

		buttonDiv.animate({
			opacity: '1'
		}, { 
			duration: speed*2, queue: false 
		});
	};

	// Montors left and right arrow key events
	$("body").keydown(handleKeyPress);

}

function handleKeyPress (e) {
  if(e.which == 37) { // left     
      slideInBackAndReplace();
      console.log("left key pressed");
  }
  else if(e.which == 39) { // right     
      slideOutFrontAndReplace();
      console.log("right key pressed");
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
		$(".expButImg").addClass("upsideDown");
		theBox.fadeIn(300, function(){
			theBox.removeClass('closed');
		});
	}else{
		$(".expButImg").removeClass("upsideDown");
		theBox.fadeOut(300, function(){
			theBox.addClass('closed');
		});
	};
}

// Set text card num
function updateCardNumText () {
	var finalString = cardNumCodeTextField.replace('%current%', currentCardNum).replace('%total%', totalCardNum);
	$("#cardNumTag").html(finalString);
}

// Function to animate the cards sliding out front to back
function slideOutFrontAndReplace () {
	if (!isTransitioningCard) {
		isTransitioningCard = true;
		smoothScroll();
		var frontCard = $('.frontResult');
		var secondCard = frontCard.next();
		

		frontCard.animate({
	       left: '-150%'
	    }, { duration: 500, queue: false, complete: function(){
	    	frontCard.removeClass('frontResult');
	    	secondCard.addClass('frontResult');
	    	frontCard.css({
	    		left: '',
	    		opacity: '0',
	    		display: 'none'
	    	});
	    	frontCard = frontCard.detach();
	    	resultsView.append(frontCard);
	    	// Update counter
			currentCardNum = currentCardNum+1;
			currentCardNum == totalCardNum+1 ? currentCardNum = 1: currentCardNum = currentCardNum;
			updateCardNumText();
			isTransitioningCard = false;
	    } });

		secondCard.css('display', 'block');
	    secondCard.animate({
	       opacity: '1'
	    }, { duration: 500, queue: false });
	};
}

function slideInBackAndReplace () {
	if (!isTransitioningCard) {
		isTransitioningCard = true;
		smoothScroll();
		var frontCard = $('.frontResult');
		var backCard = frontCard.parent().children(":last");


		frontCard.animate({
	       opacity: '0'
	    }, { duration: 500, queue: false, complete: function(){
	    	frontCard.removeClass('frontResult');
	    	backCard.addClass('frontResult');
	    	backCard.css({
	    		opacity: '',
	    		left: '',
	    		display: ''
	    	});
	    	frontCard.css({
	    		opacity: '',
	    		left: '',
	    		display: ''
	    	});
	    	backCard = backCard.detach();
	    	resultsView.children("a").last().after(backCard);
	    	// Update counter
			currentCardNum = currentCardNum-1;
			currentCardNum == 0 ? currentCardNum = totalCardNum: currentCardNum = currentCardNum;
			updateCardNumText();
			isTransitioningCard = false;
	    } });

		backCard.css({
			left:'-150%',
			opacity: '1',
			display: 'block'
		});
	    backCard.animate({
	       left: '0%'
	    }, { duration: 500, queue: false });
	};
}


// Function to smoothscroll to top of element
function smoothScroll () {
	var offsetTop = $('.resultSlider.frontResult').offset().top-10;

	if (offsetTop < 0) {
		resultsView.animate({
            scrollTop: offsetTop
        }, { duration: 500, queue: false });
	};
	
}

// Helper function to see if a parameter is empty. Returns true if not empty
function checkParamValues (param) {
	return !(param==''||param==undefined||param==null);
}

// Attach function to calButton (calendar event)
function setUpClickOnCalButton () {
	$('.calButton').click(function(event){
		event.preventDefault();

		var queryString = '/api/calendarExport?htmlPage=';

		var htmlContent = $(this).parents("tr").parent().children('.calData').html();

		// console.log(htmlContent);

		window.open(queryString+encodeURIComponent(htmlContent.trim()), '_blank');

	});
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

// Autocomplete setup
$("input[name='p2pFrom']").autocomplete({
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
$("input[name='p2pTo']").autocomplete({
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