$(function() {
	$('html').niceScroll({
		cursorborder: 'none',
		cursorwidth: '8px',
		cursoropacitymin: '0.5',
		railpadding: {top: 4, right: 4, left: 0, bottom: 4},
		bouncescroll: true,
		cursorcolor: "#666",
	});

	$('.top_menu .btn').on('click', function() {
		$('.top_menu .btn').attr('class', 'btn');
		$(this).attr('class', 'btn active');
		if($(this).attr('id') == 'articles_new') {
			$('.articles.popular').css('display', 'none');
			$('.articles.new').css('display', 'block');
		} else if($(this).attr('id') == 'articles_popular') {
			$('.articles.new').css('display', 'none');
			$('.articles.popular').css('display', 'block');
		}
	});
});