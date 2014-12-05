$('a.homepage').click(function(event){
	//stop link from being followed
	event.preventDefault();

	// Make the 'a' element the same size as its child so that it forces the other blocks to stay in place
	$(this).css({
		width: $(this).children('div').outerWidth(true)+'px',
		height: $(this).children('div').outerHeight(true)+'px',
		float: 'left'
	});

	// Frequently referenced
	var theLink = $(this).attr('href');
	var overlayView = $('#overlayView');
	var flipDiv = $(this).children('div');

	// Save offset before changing anything, make sure the box starts in the right place
	flipDivOffset = flipDiv.offset();
	
	// move the box to the overlay view and show
	overlayView.append(flipDiv);
	overlayView.removeClass('hidden');
	
	// Create a new stylesheet and position the box in its old location
	addStylesheetRules([
		['.box.flip, .box2.flip', // Also accepts a second argument as an array of arrays instead
			['left', flipDivOffset.left+'px'],
			['top', flipDivOffset.top+'px']
		]
	]);


	// Start the flip
	flipDiv.addClass('flip');

	// Stop scrollbars from showing and scrolling
	$('body').css('overflow', 'hidden');

	// Parse the new background colour
	var backgroundColor = flipDiv.children().children('.front').css('background-color');

	// Set background colour of the box
	flipDiv.css('background-color', backgroundColor);

	// Hide front panel to show the back
	flipDiv.children('.flipper').children('.front').css('visibility','hidden');

	// After delay (same time as flipping animation duration+delay), set the body's new bgcolour, then get resource
	setTimeout(function(){
		setBGColour(backgroundColor);
		requestThenFadeOut(theLink);
	}, 800);


	return false;
});


function requestThenFadeOut (theLink) {

	// Often used
	var overlayView = $('#overlayView');

	// Start Ajax
	sendAjaxRequest(theLink, function(data){
		// Set contentDiv to new page
		replaceHTMLOfElement ($('#contentDiv'), data);

		// Start fadeOut of overlay
		overlayView.addClass('fadeOut');

		// Set the overflow of body to its previous value
		$('body').css('overflow', 'initial');
		
		// After all animations have finished, reset the overlay
		setTimeout(function(){
			overlayView.addClass('hidden');
			overlayView.removeClass('fadeOut');
			overlayView.html('');
		}, 1100);
	});
}