from django.shortcuts import render, redirect
from django.views.generic import View, DetailView, CreateView
from django.urls import reverse_lazy, reverse

from .models import *
from .forms import *
from account.utils import MessagesMixin

bad_words = [
	'perdun', 'kaka', 'kakashka', 'idiot', 'durak',
	'пердун', 'кака', 'какашка', 'идиот', 'дурак', 'дурачина',
]

class AllArticlesView(View):
	def get(self, request):
		context = {
			'articles': Article.objects.filter(is_available = True).order_by('-date'),
			'articles_popular': Article.objects.order_by('-likes'),
		}
		return render(request, 'it_articles/all_articles.html', context)

class DetailArticleView(DetailView):
	template_name = 'it_articles/detail.html'
	model = Article
	context_object_name = 'article'

class DetailArticleView(MessagesMixin, View):
	def get(self, request, pk):
		context = {
			'article': Article.objects.get(id = pk, is_available = True),
			'comments': Article.objects.get(id = pk, is_available = True).comments.order_by('-date'),
		}
		return render(request, 'it_articles/detail.html', context)

	def post(self, request, pk):
		text = request.POST.get('text')
		if text.strip():
			go = True
			for i in text.lower().split():
				if i in bad_words:
					go = False
					break
			'''for i in bad_words:
				if text.lower().find(i) > 0:
					print(text.lower().find(i))
					go = False
					break'''
			if go:
				comment = Comment()
				comment.user = request.user
				comment.text = text
				comment.article = Article.objects.get(id = pk)
				comment.save()
			else:
					self.set_error_msg('You writed the bad word')
		return redirect(reverse('it_articles:detail', kwargs = {'pk': pk}))


class SearchView(View):
	def get(self, request):
		context = {
			'articles': Article.objects.filter(title__contains = (request.GET.get('text')))
		}
		return render(request, 'it_articles/all_articles.html', context)