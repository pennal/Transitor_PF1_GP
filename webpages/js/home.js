$('a.homepage').click(function(event){
	event.preventDefault();

	var theLink = $(this).attr('href');

	var flipDiv = $(this).children('div');

	flipDivOffset = flipDiv.offset();
	$('#containerDiv').prepend("<div id=\"loadedContentContainer\"></div>");
	$('#loadedContentContainer').append("<div id=\"loadedContent\"></div>")
	$('#loadedContentContainer #loadedContent').append(flipDiv);
	// flipDiv = $('#loadedContentContainer #loadedContent div');
	flipDiv.addClass('flip');
	$('body').css('overflow', 'hidden');
	var backgroundColor = flipDiv.children().children('.front').css('background-color');
	flipDiv.css('background-color', backgroundColor);
	flipDiv.animate({
		width: $(document).width(),
		height: $(document).height(),
		left: (-flipDivOffset.left),
		top: (-flipDivOffset.top)
	}, 600, function(){
		flipDiv.children('.flipper').children('.front').css('visibility','hidden');
		$('.p2pBox').css({
			'background-size':'initial',
			'background-repeat':'no-repeat',
			'background-position':'center'
		});
		setBGColour(backgroundColor);
		requestThenFadeOut(theLink);
	});

	return false;
});


function requestThenFadeOut (theLink) {
	sendAjaxRequest(theLink, function(data){
		replaceHTMLOfElement ($('#contentDiv'), data);
		$('#loadedContentContainer').delay(500).fadeOut(800, function(){
			$('#loadedContentContainer').remove();
		});
		$('body').css('overflow', 'initial');
	});
}