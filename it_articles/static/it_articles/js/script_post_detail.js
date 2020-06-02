$(function() {
	$('#comment-text').keyup(function(event) {
		if(event.keyCode == 13) 
			check_comment_send();
	});
});

function delete_comment(id, url) {
	if(confirm('Вы уверены, что хотите удалить этот комментарий?')) {
		$.ajax({
			type: 'GET',
			url: url,
			data: {
				'id': id,
			},
			dataType: 'json',
			success: function() {
				$('#comment-' + id).remove();
				$('#articles-count').text(Number($('#articles-count').text()) - 1);
			},
			error: function(data) {
				alert('Ошибка ' + data.status + ' (' + data.statusText + '): ');
			}
		});
	}
}

function send_comment(post_id, url, url_delete_comment, username, img_url) {
	var text = $('#comment-text').val().replace(/ +/g, ' ').trim();
	if(text != '') {
		$.ajax({
			type: 'get',
			url: url,
			data: {
				'post_id': post_id,
				'text': text,
			}, 
			dataType: 'json',
			success: function(data) {
				var comment = $('<li id="comment-' + data.id + '"><img src="' + img_url + '"><div class="comment"><div class="user"><div><div>' + username + '</div><div class="date">' + data.date + '</div></div><i class="fa fa-times" aria-hidden="true" onclick="delete_comment(' + data.id + ', ' + "'" + url_delete_comment + "'" +  ')"></i></div><div class="text">' + data.text + '</div></div></li>');
				$('.comments ul').prepend(comment);
				$('#comment-text').val('');
				$('#articles-count').text(Number($('#articles-count').text()) + 1);
			},
			error: function(data) {
				alert('Ошибка ' + data.status + ' (' + data.statusText + '): ' + data.responseJSON.info);
			},
		});
	}
}