$(function() {
	$('.help-buttons button').on('click', function() {
		var prev_val = $('.new-article-form textarea').val();
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
			new_val = '<ul><li>ЗНАЧЕНИЕ 1</li><li>ЗНАЧЕНИЕ 2</li><li>ЗНАЧЕНИЕ 3</li></ul>'
			break;
		case 'help-btn-list-ol':
			new_val = '<ol><li>ЗНАЧЕНИЕ 1</li><li>ЗНАЧЕНИЕ 2</li><li>ЗНАЧЕНИЕ 3</li></ol>'
			break;
		case 'help-btn-link':
			new_val = '<a href="АДРЕС">ССЫЛКА</a>';
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

		$('.new-article-form textarea').val(prev_val + new_val);
	});
});

function text_transform() {
	var text = val = $('.new-article-form textarea').val();
	$('#post-view').html(text);
}

/*function new_text() {
			var val = $('.new-article-form textarea').val();
				var lang_python = false;
				var lang_cmd = false;
				var small_code = false;
				var word = false;
				var link = [false, false];
				var header = false;
				$('#post-view').text('');
				for(var i = 0; i < val.length; i++) {
					if(val[i] == '`') {
						if(!lang_python) {
							lang_python = true;
							$('#post-view').append('<pre class="code"><code class="language-python">');
						} else {
							lang_python = false;
							$('#post-view').append('</a');
						}
					} else if(val[i] == '~') {
						if(!small_code) {
							small_code = true;
							$('#post-view').append('<span class="post-small-code">');
						} else {
							small_code = false;
							$('#post-view').append('</span>');
						}
					} else if(val[i] == '|') {
						if(!word) {
							word = true;
							$('#post-view').append('<span class="post-word">');
						} else {
							word = false;
							$('#post-view').append('</span>');
						}
					} else if(val[i] == '^') {
						if(!link[0]) {
							link[0] = true;
							link[1] = true;
							$('#post-view').append('<a>');
						} else if(link[1]) {
							link[1] = false
						} else {
							link[0] = false;
							$('#post-view').append('</a>');
						}
					} else if(val[i] == '*' && val[i + 1] == '*') {
						i++;
						if(!header) {
							header = true;
							$('#post-view').append('<span class="post-header">');
						} else {
							header = false;
							$('#post-view').append('</span>');
						}
					} else {
						if(lang_python) {
							$('#post-view').children().eq($('#post-view').children().length - 1).children(0).append(val[i]);
						} else if(small_code || word || header) {
							$('#post-view').children().eq($('#post-view').children().length - 1).append(val[i]);
						} else if(link[0]) {
							if(link[1]) {
								prev = $('#post-view').children().eq($('#post-view').children().length - 1).attr('href');
								if(!prev)
									prev = '';
								$('#post-view').children().eq($('#post-view').children().length - 1).attr('href', prev + val[i]);
							} else {
								$('#post-view').children().eq($('#post-view').children().length - 1).append(val[i]);
							}
						} else
							$('#post-view').append(val[i]);
					}
				}
		}*/