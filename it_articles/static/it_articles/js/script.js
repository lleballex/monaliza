function like(id, url, detail = false) {
	$.ajax({
		type: 'get',
		url: url,
		data: {
			'id': id,
		},	
		dataType: 'json',
		success: function(data) {
			$('#like-' + id).toggleClass('is_liked')
			if(data.deleted) {
				if(!detail)
					$('#like-' + id + ' .fa').attr('class', 'fa fa-thumbs-o-up');
				else 
					$('#like-' + id + ' .fa').attr('class', 'fa fa-heart-o');
				$('#like-' + id + ' span').text(Number($('#like-' + id + ' span').text()) - 1);
			} else if(data.created) {
				if(!detail)
					$('#like-' + id + ' .fa').attr('class', 'fa fa-thumbs-up');
				else
					$('#like-' + id + ' .fa').attr('class', 'fa fa-heart');
				$('#like-' + id + ' span').text(Number($('#like-' + id + ' span').text()) + 1);
			}
		},
		error: function(data) {
			alert('Ошибка ' + data.status + ' (' + data.statusText + '): ' + data.responseJSON.info);
		},
	});
}
