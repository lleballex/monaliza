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

function delete_answer(id, url) {
	if(confirm('Вы уверены, что хотите удалить свой ответ?'))
		$.ajax({
			type: 'get',
			url: url,
			data: {
				'id': id,
			},
			dataType: 'text',
			success: function(data) {
				if(data == '200')
					$('#answer-' + id).remove();
				else
					alert(data)
			},
		});	
}

function set_right_answer(id, url, is_right_answer) {
	if(confirm(is_right_answer ? 'Вы уверены, что этот ответ не является решением вопроса?' : 'Вы точно хотите отметить этот ответ решением вопроса?'))
		$.ajax({
			type: 'get',
			url: url,
			data: {
				'id': id,
			},
			dataType: 'text',
			success: function(data) {
				if(data == '200') {
					for(var i = 0; i < $('.answers ul').children().length; i++) 
						if($('.answers ul').children().eq(i).attr('class') == 'right-answer')
							$('.answers ul').children().eq(i).toggleClass('right-answer');
					
					if(!is_right_answer)
						$('#answer-' + id).addClass('right-answer');
					else
						$('#answer-' + id).removeClass('right-answer');
				} else
					alert(data);
			},
		});	
}