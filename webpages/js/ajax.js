$(document).ready(function(){

	// Variable containing the div which always gets updated
	var contentDiv = $('#contentDiv');

	// Function to send GET Ajax request
	function sendAjaxRequest (url, requestString, callback) {
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
		  	console.log('readyState: '+xmlhttp.readyState+', code: '+xmlhttp.status);
		  }

		}

		// Build request
		xmlhttp.open("GET",url+'?'+requestString,true);

		// Show the loading bar
		showLoadingAjax();
		
		// Finally submit the request
		xmlhttp.send();
	}

	// Helper method to replace an element's HTML
	function replaceHTMLOfElement (element, content) {
		element.html(content);
	}


	// Sends Ajax request and puts returned content into the contentDiv
	function setupAndSendAjaxRequest (requestedPage, requestString) {
		sendAjaxRequest(requestedPage, requestString, function(data){
			replaceHTMLOfElement(contentDiv, data);
		});
	}

	// Prepare to show loading screen
	function showLoadingAjax () {
		replaceHTMLOfElement(contentDiv, '');
		showProgressBar();
	}

	// Update progress bar
	function updateProgressBar (percent) {
		$("#progressDiv #innerProgress").css('width', ''+percent+'%');
	}

	// Unhide progress bar
	function showProgressBar () {
		$("#progressDiv").css('display', 'block');
	}

	// Hide progress bar
	function hideProgressBar () {
		$("#progressDiv").css('display', 'none');
	}

	// Test to get a page's content
	setupAndSendAjaxRequest('pages/p2p/input.html', '');

});