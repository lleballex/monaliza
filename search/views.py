from django.shortcuts import render
from django.views.generic import View

from it_articles.models import Article

class SearchView(View):
	def get(self, request):
		text = request.GET.get('text')
		model = request.GET.get('model')
		template_name = 'it_articles/all_articles.html'

		context = {'articles': None}

		if model == 'post':
			context['articles'] = Article.objects.filter(title__contains = text)
			template_name = 'it_articles/all_articles.html'

		return render(request, template_name, context)
