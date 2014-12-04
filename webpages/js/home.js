$('a.homepage').click(function(event){
	event.preventDefault();

	$(this).css({
		width: $(this).children('div').outerWidth(true)+'px',
		height: $(this).children('div').outerHeight(true)+'px',
		float: 'left'
	});
	var theLink = $(this).attr('href');
	var overlayView = $('#overlayView');
	var flipDiv = $(this).children('div');

	flipDivOffset = flipDiv.offset();
	// $('#containerDiv').prepend("<div id=\"loadedContentContainer\"></div>");
	// $('#loadedContentContainer').append("<div id=\"loadedContent\"></div>");
	
	overlayView.append(flipDiv);
	overlayView.removeClass('hidden');
	// flipDiv.css({
	// 	position: 'absolute',
	// 	left: (flipDivOffset.left),
	// 	top: (flipDivOffset.top)
	// });
	
	addStylesheetRules([
		['.box.flip, .box2.flip', // Also accepts a second argument as an array of arrays instead
			['left', flipDivOffset.left+'px'],
			['top', flipDivOffset.top+'px'] // 'true' for !important rules 
		]
	]);


	flipDiv.addClass('flip');

	// flipDiv.css({
	// 	left:'0px',
	// 	top: '0px'
	// });

	// flipDiv.children().children().css({
	// 	'background-size':'initial',
	// 	'background-repeat':'no-repeat',
	// 	'background-position':'center'
	// });

	$('body').css('overflow', 'hidden');
	var backgroundColor = flipDiv.children().children('.front').css('background-color');
	flipDiv.css('background-color', backgroundColor);
	flipDiv.children('.flipper').children('.front').css('visibility','hidden');


	setTimeout(function(){
		setBGColour(backgroundColor);
		requestThenFadeOut(theLink);
	}, 800);


	return false;
});


function requestThenFadeOut (theLink) {
	var overlayView = $('#overlayView');
	sendAjaxRequest(theLink, function(data){
		replaceHTMLOfElement ($('#contentDiv'), data);
		overlayView.addClass('fadeOut');
		$('body').css('overflow', 'initial');
	});
}