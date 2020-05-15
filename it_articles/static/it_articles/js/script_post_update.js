$(function() {
	$('.help-buttons button').on('click', function() {
		var new_val = '';
		var new_vals = [];
		var start = textarea.selectionStart;
		var end = textarea.selectionEnd;
		var selection = false;

		if(start != end)
			selection = true;

		switch($(this).attr('id')) {
		case 'help-btn-header':
			if(selection){
				new_vals[0] = '<span class="post-header">';
				new_vals[1] = '</span>'
			} else
				new_val = '<span class="post-header">ЗАГОЛОВОК</span>';
			break;
		case 'help-btn-paragraph':
			if(selection) {
				new_vals[0] = '<br>';
				new_vals[1] = '';
			} else
				new_val = '<br>'
			break;
		case 'help-btn-code-small':
			if(selection) {
				new_vals[0] = '<span class="post-small-code">';
				new_vals[1] = '</span>'
			} else {
				code = prompt('То, что вы считаете кодом:');
				if(!code)
					code = 'КОД';
				new_val = '<span class="post-small-code">' + code + '</span>';
			}
			break;
		case 'help-btn-code':
			if(selection) {
				new_vals[0] = '<pre class="code"><code class="langauge-python">'
				new_vals[1] = '</code></pre>';
			} else 
				new_val = '<pre class="code"><code class="language-python">КОД</code></pre>';
			break;	
		case 'help-btn-word':
			if(selection) {
				new_vals[0] = '<span class="post-word">';
				new_vals[1] = '</span>'
			} else {
				word = prompt('Что вы хотите выделить?');
				if(!word)
					word = 'ВЫДЕЛЕНИЕ';
				new_val = '<span class="post-word">' + word + '</span>';
			}
			break;
		case 'help-btn-list-ul':
			if(selection) {
				new_vals[0] = '<li>';
				new_vals[1] = '</li>';
			} else {
				new_val = '<ul>'
				var num = prompt('Сколько значений необходимо создать в списке?');
				for(var i = 0; i < num; i++)
					new_val += '<li>ЗНАЧЕНИЕ ' + (i + 1) + '</li>';
				new_val += '</ul>';
			}
			break;
		case 'help-btn-list-ol':
			if(selection) {
				new_vals[0] = '<li>';
				new_vals[1] = '</li>'
			} else {
				new_val = '<ol>'
				var num = prompt('Сколько значений необходимо создать в списке?');
				for(var i = 0; i < num; i++)
					new_val += '<li>ЗНАЧЕНИЕ ' + (i + 1) + '</li>';
				new_val += '</ol>';
			}
			break;
		case 'help-btn-link':
			if(selection) {
				var addr = prompt('Какой будет адресс у этой ссылки?');
				if(!addr)
					addr = 'АДРЕСС';
				new_vals[0] = '<a href="' + addr + '">';
				new_vals[1] = '</a>';
			} else {
				var addr = prompt('Адресс ссылки:');
				var link = prompt('Сама ссылка:');
				if(!addr)
					addr = 'АДРЕСС';
				if(!link)
					link = 'ССЫЛКА';
				new_val = '<a href="' + addr + '">' + link + '</a>';
			}
			break;
		case 'help-btn-image':
			if(selection) {
				var width = prompt('Ширина в пикселях (чтобы не менять ширину, ничего не вводите):');
				var height = prompt('Высота в пикселях (чтобы не менять высоту, ничего не вводите):');
				new_vals[0] = '<img src="';
				new_vals[1] = '"';
				if(width)
					new_vals[1] += ' width="' + width + 'px"';
				if(height)
					new_vals[1] += ' height="' + height + 'px"';
				new_vals[1] += '>';
			} else {
				var src = prompt('Адрес картинки: ');
				var width = prompt('Ширина в пикселях (чтобы не менять ширину, ничего не вводите):');
				var height = prompt('Высота в пикселях (чтобы не менять высоту, ничего не вводите):');
				if(!src)
					src = 'АДРЕСС';
				new_val = '<img src="' + src + '"';
				if(width)
					new_val += ' width="' + width + 'px"';
				if(height)
					new_val += ' height="' + height + 'px"';
				new_val += '>'
			}
			break;
		case 'help-btn-underline':
			if(selection) {
				new_vals[0] = '<u>';
				new_vals[1] = '</u>';
			} else {
				text = prompt('То, что вы хотите подчеркнуть: ');
				if(!text)
					text = 'ПОДЧЕРКНУТЫЙ ТЕКСТ';
				new_val = '<u>' + text + '</u>';
			}
			break;
		case 'help-btn-bold':
			if(selection) {
				new_vals[0] = '<b>';
				new_vals[1] = '</b>';
			} else {
				text = prompt('Что будет жирным текстом? ');
				if(!text)
					text = 'ЖИРНЫЙ ТЕКСТ';
				new_val = '<b>' + text + '</b>';
			}
			break;
		case 'help-btn-italic':
			if(selection) {
				new_vals[0] = '<i>';
				new_vals[1] = '</i>';
			} else {
				text = prompt('Что быдет записано курсивом?');
				if(!text)
					text = 'КУРСИВ';
				new_val = '<i>' + text + '</i>'
			}
			break;
		}

		
		if(!selection)
			textarea.setRangeText(new_val, textarea.selectionStart, textarea.selectionEnd, "end");
		else 
			textarea.value = textarea.value.substr(0, start) + new_vals[0] + textarea.value.substr(start, end - start) + new_vals[1] + textarea.value.substr(end, textarea.value.length - end);
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