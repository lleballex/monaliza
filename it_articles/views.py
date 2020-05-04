from django.shortcuts import render, redirect
from django.views.generic import View, DetailView, CreateView
from django.urls import reverse_lazy, reverse
from django.http.response import HttpResponse
import json

from .models import Article, Comment
from account.models import FavouriteArticle
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

'''class DetailArticleView(DetailView):
	template_name = 'it_articles/detail.html'
	model = Article
	context_object_name = 'article'''

class DetailArticleView(MessagesMixin, View):
	def get(self, request, pk):
		if request.user.is_superuser:
			article = Article.objects.get(id = pk)
		else:
			article = Article.objects.get(id = pk, is_available = True)
		context = {
			'article': article,
			'comments': Article.objects.get(id = pk).comments.order_by('-date'),
		}
		article.views += 1;
		article.save()
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

class SendComment(View):
	def get(self, request, pk):
		text = request.GET.get('text')
		comment = Comment()
		comment.user = request.user
		comment.text = text
		comment.article = Article.objects.get(id = pk)
		comment.save()
		context = {
			'text': comment.text,
			'date': comment.date.strftime('%B %d, %H:%M'),
			'id': comment.id,
		}
		return HttpResponse(json.dumps(context))

class DeleteComment(View):
	def get(self, request, pk):
		id = request.GET.get('id')
		try:
			comment = Comment.objects.get(id = id)
			if comment.user == request.user:
				comment.delete()
				return HttpResponse('200')
			else:
				return HttpResponse('403')
		except:
			return HttpResponse('404')

class LikeArticle(View):
	def get(self, request):
		id = request.GET.get('id')
		try:
			article = Article.objects.get(id = id)
			fav_article = FavouriteArticle.objects.get(article = article)
			fav_article.delete()
			article.likes -= 1
			article.save()
			return HttpResponse('EXIST')
		except:
			article = Article.objects.get(id = id)
			fav_article = FavouriteArticle()
			fav_article.article = article
			fav_article.user = request.user
			fav_article.save()
			article.likes += 1
			article.save()
			return HttpResponse('DOES_NOT_EXIST')