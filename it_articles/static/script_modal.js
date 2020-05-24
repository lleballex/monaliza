$(function() {
	$('.start-modal-btn').on('click', function() {
		//$('.modal').css('display', 'block');
		var a = modal([1]);
		alert(a);
	});
	/*$('.modal-header').on('click', 'button', function() {
		$('.modal').css('display', 'none');
	});*/
});

function modal(args) {
	var answers = [];
	for(var i = 0; i < args.length; i++) {
		$('.modal-body').append('<label>' + args[i] + '</label>' + '<input type="text">');
	}
	$('.modal').css('display', 'block');
	while(true) {
		var quit = false;
		$('.modal-header').on('click', 'button', function() {
			for(var i = 0; i < args.length; i++) {
				answers.push($('.modal-body input').eq(i).val());
			}
			$('.modal').css('display', 'none');
			alert(answers);
			quit = true;
		});
		if(quit)
			break;
	}
	return answers;
}