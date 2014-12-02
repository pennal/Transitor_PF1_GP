$(document).ready(function(){

	var contentDiv = $('#contentDiv');

	function sendAjaxRequest (url, callback) {
		var xmlhttp;
		if (window.XMLHttpRequest)
		  {// code for IE7+, Firefox, Chrome, Opera, Safari
		  xmlhttp=new XMLHttpRequest();
		  }
		else
		  {// code for IE6, IE5
		  xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
		  }

		xmlhttp.onprogress = function(e){
		    if (e.lengthComputable){
		    	var progress = (e.loaded / e.total) * 100;
		        updateProgressBar(progress);
		    }
		};

		xmlhttp.onreadystatechange=function(){
		  
		  if (xmlhttp.readyState==4 && (xmlhttp.status==200||xmlhttp.status==0)) {
		  	hideProgressBar();
		  	updateProgressBar(0);
		  	callback(xmlhttp.responseText);
		  }else{
		  	console.log('readyState: '+xmlhttp.readyState+', code: '+xmlhttp.status);
		  }

		}
		xmlhttp.open("GET",url,true);
		showLoadingAjax();
		xmlhttp.send();
	}

	function replaceHTMLOfElement (element, content) {
		element.html(content);
	}

	function setupAndSendAjaxRequest (requestedPage) {
		sendAjaxRequest(requestedPage, function(data){
			console.log('data= '+data)
			replaceHTMLOfElement(contentDiv, data);
		});
	}

	function showLoadingAjax () {
		replaceHTMLOfElement(contentDiv, '');
		showProgressBar();
	}

	function updateProgressBar (percent) {
		$("#progressDiv #innerProgress").css('width', ''+percent+'%');
	}

	function showProgressBar () {
		$("#progressDiv").css('display', 'block');
	}

	function hideProgressBar () {
		$("#progressDiv").css('display', 'none');
	}

	setupAndSendAjaxRequest('files/test.txt');

});