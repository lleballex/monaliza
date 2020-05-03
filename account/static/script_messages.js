$(function() {
	$('.messages .close').on('click', function() {
		$(this).parent().remove();
	});
});