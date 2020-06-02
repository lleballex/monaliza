$(function() {
	$('#search-search-btn').on('click', function() {
		$('.search-form input').val('');
		$('#search-close-btn').css('transform', 'scale(1)');
		$('#search-search-btn').css('transform', 'scale(0)');
	});

	$('#search-close-btn').on('click', function() {
		$('.search-form input').focus();
	});	

	$('.search-form input[type="text"]').focus(function() {
		$('.search-form').css('box-shadow', '0 0 5px 2px #bbb');
		$('#search-close-btn').css('transform', 'scale(0)');
		$('#search-search-btn').css('transform', 'scale(1)');
	});
	
	$('.search-form input[type="text"]').blur(function() {
		var val = $('.search-form input').val();
		if(val.split() == '') {
			$('#search-close-btn').css('transform', 'scale(1)');
			$('#search-search-btn').css('transform', 'scale(0)');
		}
		$('.search-form').css('box-shadow', '0 0 3px 0 #ccc');
	});		
});