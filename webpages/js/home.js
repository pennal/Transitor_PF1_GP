$('a.homepage').click(function(event){
	event.preventDefault();

	$(this).children('div').addClass('flip');

	return false;
});