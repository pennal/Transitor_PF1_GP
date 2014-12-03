$('a.homepage').click(function(event){
	event.preventDefault();

	var flipDiv = $(this).children('div');

	flipDivOffset = flipDiv.offset();
	flipDiv.addClass('flip');
	$('body').css('overflow', 'hidden');
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
	});

	sendAjaxRequest(requestedPage, function(data){
		replaceHTMLOfElement(contentDiv, data);
	});

	return false;
});