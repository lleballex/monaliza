from django.shortcuts import render, redirect
from django.views.generic import View, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.http.response import HttpResponse
import json

from .models import Article, Comment
from account.models import FavouriteArticle, Notification, User
from .forms import *
from account.utils import MessagesMixin, AccessMixin

class Redirect(View):
	def get(self, request):
		return redirect(reverse('it_articles:all_posts'))

class AllArticlesView(View):
	def get(self, request):
		context = {
			'articles': Article.objects.filter(is_available = True).order_by('-date'),
			'articles_popular': Article.objects.order_by('-likes'),
		}
		return render(request, 'it_articles/all_articles.html', context)

class DetailArticleView(AccessMixin, MessagesMixin, View):
	def get(self, request, pk):
		try:
			article = Article.objects.get(id = pk)
		except self.model.DoesNotExist:
			self.message = 'К сожалению, данного поста не существует'
			return self.mixin_render()

		if not article.is_available:
			if not request.user.is_authenticated or (not request.user == article.user and not request.user.is_superuser):
				self.message = 'К сожалению, этот пост еще не верифицирован. поэтом он вам не доступен. Вы можете подождать его верифицакии'
				self.status_code = 403
				return self.mixin_render()
			else:
				self.set_error_msg('Этот пост еще не проверен, из-за чего он пока не доступен для других пользователей')
		else:
			article.views += 1;
			article.save()

		context = {
			'article': article,
			'comments': article.comments.order_by('-date'),
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


class MyArticlesView(AccessMixin, MessagesMixin, View):
	def get(self, request):
		if not request.user.is_authenticated:
			self.status_code = 403
			self.message = 'Для доступа к данной странице необходимо авторизоваться'
			return self.mixin_render()

		likes = 0
		all_articles = 0
		views = 0
		comments = 0
		articles = Article.objects.filter(user = request.user)
		for article in articles:
			likes += article.likes
			views += article.views
			comments += article.comments.count()
			all_articles += 1

		context = {
			'articles': articles.order_by('-id'),
			'likes': likes,
			'all_articles': all_articles,
			'views': views,
			'comments': comments
		}

		return render(request, 'it_articles/my_articles.html', context)


class NewArticleView(MessagesMixin, CreateView):
	template_name = 'it_articles/edit_article.html'
	model = Article
	form_class = NewArticleForm
	success_url = reverse_lazy('posts:my_posts')
	success_msg = 'The article was successfuly created. Please wait for verification'

	def form_valid(self, form):
		self.object = form.save(commit = False)
		self.object.user = self.request.user
		#self.object.text = self.post_text(self.object.text)
		self.object.save()
		notification = Notification()
		notification.user = User.objects.get(is_superuser = True)
		notification.title = 'Был создан новый пост'
		notification.text = self.object.user.username + ' создал новый пост - <a href="' + self.object.get_absolute_url() + '">' + self.object.title + '</a>'
		notification.save()
		return super().form_valid(form)

class EditArticleView(AccessMixin, MessagesMixin, UpdateView):
	model = Article
	form_class = NewArticleForm
	template_name = 'it_articles/edit_article.html'
	success_url = reverse_lazy('posts:my_posts')
	success_msg = 'The article was successfuly updated'
	
	def get(self, request, *args, **kwargs):
		pk = kwargs.get(self.pk_url_kwarg)
		try:
			self.get_queryset().filter(pk = pk).get()
		except self.model.DoesNotExist:
			self.message = 'К соэжалению, данного поста не существует'
			return self.mixin_render()
		
		self.object = self.get_object()
		context = self.get_context_data(object=self.object)
		return self.render_to_response(context)

	def get_context_data(self, **kwargs):
		if not self.request.user.is_authenticated or self.request.user != self.get_object().user:
			self.message = 'Этот пост принадлежит другому пользователю, и только он может его редактировать!'
			self.status_code = 403
			self.access_mixin = True
		kwargs['update'] = True
		return super().get_context_data(**kwargs)

class DeleteArticleView(MessagesMixin, DeleteView):
	success_msg = 'The article was successfuly deleted'
	model = Article
	success_url = reverse_lazy('posts:my_posts')