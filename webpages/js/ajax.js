$(document).ready(function(){
	documentReady()
});

// Listen for hash changes
window.addEventListener("hashchange", dealWithHash);

// Variable containing the div which always gets updated
var contentDiv

var isAnimatingPageChange = false

// Function to send GET Ajax request
function sendAjaxRequest (url, callback) {
	if (true) {};
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
	  	window.location.hash = url
	  	callback(xmlhttp.responseText);
	  }else{
	  	// console.log('readyState: '+xmlhttp.readyState+', code: '+xmlhttp.status);
	  }

	}

	// Build request
	xmlhttp.open("GET",url,true);

	// Show the loading bar
	showLoadingAjax();
	
	// Finally submit the request
	xmlhttp.send();
}

// Sets up environment after new load
function newPageSetup () {
	// Take the title from the webpage
	var newTitle = $('div.title.hidden').html();
	if (newTitle != undefined) {
		document.title = newTitle
		$('div.title.hidden').remove();
	};

	// Intercept clicks on internal links - new watcher has to be made to apply to the new links
	$('a.internal:not(.homepage)').click(function(event){
		event.preventDefault();
		setupAndSendAjaxRequest($(this).attr('href'));
		return false;
	});
}

// Helper method to replace an element's HTML
function replaceHTMLOfElement (element, content, animated) {

	// Set the new content either animated or not
	if (animated) {
		isAnimatingPageChange = false;
		element.prepend("<div id=\"loadedContent\"></div>");
		$('#loadedContent').html(content);
		element.animate({
			opacity:0
		}, 300, function(){
			// element.html(content);
			// element.css('opacity', '1');
			// $('#loadedContent').remove();
			newPageSetup();
		})
	} else{
		element.html(content);
		newPageSetup();
	};
}


// Sends Ajax request and puts returned content into the contentDiv
function setupAndSendAjaxRequest (requestedPage) {
	sendAjaxRequest(requestedPage, function(data){
		replaceHTMLOfElement(contentDiv, data, false);
	});
}

// Prepare to show loading screen
function showLoadingAjax () {
	// replaceHTMLOfElement(contentDiv, '', false);
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

// Parses hash and redirects if needed
function dealWithHash () {
	var hash = window.location.hash.substr(1);
	console.log('Hash changed to: '+hash);
	if (!isAnimatingPageChange) {
		if (hash != '') {
			setupAndSendAjaxRequest(hash);
		}else{
			setupAndSendAjaxRequest('pages/home.html');
		}
	};
}

// Called when page has loaded
function documentReady () {
	contentDiv = $('#contentDiv');

	// Test to get a page's content
	// setupAndSendAjaxRequest('files/test.txt');

	// When first loaded (after function definitions), check to see if it needs to redirect you because of a hash
	dealWithHash();
}