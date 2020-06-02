$(function() {
	$('.answer-views button').on('click', function() {
		if($(this).attr('class') != 'active') {
			$('.answer-views button').toggleClass('active');
			$('.form-view').toggleClass('active');
			$('.answer-view').toggleClass('active');

			if($(this).attr('id') == 'answer-form-view')
				$('.answer-view').html($('.form-view textarea').val());
			}
		});

		$('.help-buttons button').on('click', function() {
		var prev_val = $('.form-view textarea').val();
		var new_val = '';

		switch($(this).attr('id')) {
		case 'help-btn-header':
			new_val = '<span class="post-header">ЗАГОЛОВОК</span>';
			break;
		case 'help-btn-paragraph':
			new_val = '<br>'
			break;
		case 'help-btn-code-small':
			new_val = '<span class="post-small-code">КОД</span>';
			break;
		case 'help-btn-code':
			new_val = '<pre class="code"><code class="language-python">КОД</code></pre>';
			break;	
		case 'help-btn-word':
			new_val = '<span class="post-word">ВЫДЕЛЕНИЕ</span>';
			break;
		case 'help-btn-list-ul':
			new_val = '<ul>';
			var num = prompt("Сколько значений в списке надо создать?");
			for(var i = 0; i < num; i++) 
				new_val += '<li>ЗНАЧЕНИЕ ' + (i + 1) + '</li>';
			new_val += '</ul>'
			break;
		case 'help-btn-list-ol':
			new_val = '<ol>';
			var num = prompt("Сколько значений в списке надо создать?");
			for(var i = 0; i < num; i++) 
				new_val += '<li>ЗНАЧЕНИЕ ' + (i + 1) + '</li>';
			new_val += '</ol>'
			break;
		case 'help-btn-link':
			var addr = prompt('Адрес страницы:');
			var link = prompt('Сама ссылка:');
			new_val = '<a href="' + addr + '">' + link + '</a>';
			break;
		case 'help-btn-underline':
			new_val = '<u>ПОДЧЕРКНУТЫЙ ТЕКСТ</u>'
			break;
		case 'help-btn-bold':
			new_val = '<b>ЖИРНЫЙ ТЕКСТ</b>'
			break;
		case 'help-btn-italic':
			new_val = '<i>КУРСИВ</i>'
			break;
		}
		$('.form-view textarea').val(prev_val + new_val);
	});
});

function answer_send(url, question_id) {
	var text = $('.form-view textarea').val();
	$.ajax({
		type: 'get',
		url: url,
		data: {
			'question_id': question_id,
			'text': text,
		},
		dataType: 'json',
		success: function(data) {
			alert('Ваш ответ успешно отправлен');
			$('.form-view textarea').val('');
			$('.answers ul').append(data.html);
		},
		error: function(data) {
			alert('Ошибка ' + data.status + ' (' + data.statusText + ') - ' + data.responseJSON.info);
		}
	});
}

function answer_delete(url, id) {
	if(confirm('Вы уверены, что хотите удалить свой ответ?'))
		$.ajax({
			type: 'get',
			url: url,
			data: {
				'id': id,
			},
			dataType: 'json',
			success: function(data) {
				$('#answer-' + id).remove();
			},
			error: function(data) {
				alert('Ошибка ' + data.status + ' (' + data.statusText + ') - ' + data.responseJSON.info);
			}
		});	
}

function answer_right(url, id, is_right_answer) {
	if(confirm(is_right_answer ? 'Вы уверены, что этот ответ не является решением вопроса?' : 'Вы точно хотите отметить этот ответ решением вопроса?'))
		$.ajax({
			type: 'get',
			url: url,
			data: {
				'id': id,
			},
			dataType: 'json',
			success: function(data) {
				if(!is_right_answer) {
					var parameters = $('.right-answer .user i').eq(0).attr('onclick');
					if(parameters) {
						parameters = parameters.split(',');
						parameters[2] = ' false)';
						$('.right-answer .user i').eq(0).attr('onclick', parameters.toString());
						$('.answers .right-answer').removeClass('right-answer');
					}
					parameters = $('#answer-' + id + ' .user i').eq(0).attr('onclick').split(',');
					parameters[2] = ' true)';
					$('#answer-' + id + ' .user i').eq(0).attr('onclick', parameters.toString());	
				} else {
					var parameters = $('#answer-' + id + ' .user i').eq(0).attr('onclick').split(',');
					parameters[2] = ' false)';
					$('#answer-' + id + ' .user i').eq(0).attr('onclick', parameters.toString());	
				}
				$('#answer-' + id).toggleClass('right-answer');
			},
			error: function(data) {
				alert('Ошибка ' + data.status + ' (' + data.statusText + ') - ' + data.responseJSON.info);
			}
		});	
}
