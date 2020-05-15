from django import forms

from it_articles.models import Article

class NewArticleForm(forms.ModelForm):
	class Meta:
		model = Article
		fields = ['title', 'text']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['text'].help_text = '''<ul class="help-buttons">
			<li><button id="help-btn-header" type="button" title="Заголовок"><i class="fa fa-header"></i></button></li>
			<li><button id="help-btn-paragraph" type="button" title="Перенос строки"><i class="fa fa-paragraph"></i></button></li>
			<li><button id="help-btn-code-small" type="button" title="Однострочный код"><i class="fa fa-code"></i></button></li>
			<li><button id="help-btn-code" type="button" title="Многострочный код"><i class="fa fa-list-alt"></i></button></li>
			<li><button id="help-btn-word" type="button" title="Выделение"><i class="fa fa-pencil"></i></button></li>
			<li><button id="help-btn-list-ul" type="button" title="Ненумерованный список"><i class="fa fa-list-ul"></i></button></li>
			<li><button id="help-btn-list-ol" type="button" title="Нумерованный список"><i class="fa fa-list-ol"></i></button></li>
			<li><button id="help-btn-link" type="button" title="Ссылка"><i class="fa fa-link"></i></button></li>
			<li><button id="help-btn-image" type="button" title="Картинка"><i class="fa fa-image"></i></button></li>
			<li><button id="help-btn-underline" type="button" title="Подчеркнутый текст"><i class="fa fa-underline"></i></button></li>
			<li><button id="help-btn-bold" type="button" title="Жирный текст"><i class="fa fa-bold"></i></button></li>
			<li><button id="help-btn-italic" type="button" title="Текст курсивом"><i class="fa fa-italic"></i></button></li>
		</ul>'''
		self.fields['text'].label = 'Содержание'
		self.fields['title'].label = 'Название'
		self.fields['text'].widget.attrs.update({'id': 'textarea'})
		'''<ul class="help-buttons">
			<li><input id="help-btn-title" type="button" value="Заголовок"></li>
			<li><input id="help-btn-code" type="button" value="Большой код"></li>
			<li><input id="help-btn-code-small" type="button" value="Маленький код"></li>
			<li><input id="help-btn-word" type="button" value="Выделение"></li>
			<li><input id="help-btn-link" type="button" value="Адрес"></li>
		</ul>'''