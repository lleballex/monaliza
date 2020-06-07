from django.shortcuts import render, redirect
from django.views.generic import View, DetailView, ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.http import Http404

from .models import Article
from account.models import FavouriteArticle, Notification, User
from qna.models import Tag
from .forms import *
from account.utils import MessagesMixin
from monaliza.utils import default_handler, AccessMixin

class PostsView(ListView):
	context_object_name = 'articles'
	template_name = 'posts/posts.html'

	def get_queryset(self):
		posts = Article.objects.filter(is_available = True).order_by('-date')
		page = self.request.GET.get('page')
		if not page:
			page = 1
		else:
			page = int(page)
		return posts[(page - 1) * 10:page * 10]

	def get_context_data(self, **kwargs):
		kwargs['articles_count'] = Article.objects.filter(is_available = True).order_by('-date').count()
		return super().get_context_data(**kwargs)

class PostView(MessagesMixin, DetailView):
	model = Article
	template_name = 'posts/post.html'
	context_object_name = 'article'

	def get(self, request, *args, **kwargs):
		self.object = self.get_object()
		if not self.object.is_available:
			if not request.user.is_superuser and request.user != self.object.user:
				return default_handler(request, 403, 'Доступ к данной странице для вас запрещен')
			self.set_error_msg('Этот пост еще не проверен и не доступен для других пользователей')
		else:
			self.object.views += 1
			self.object.save()
		context = self.get_context_data(object = self.object)
		return self.render_to_response(context)

class AvailablePost(View):
	def get(self, request, pk):
		try:
			post = Article.objects.get(id = pk)
		except:
			raise Http404
		if not request.user.is_superuser:
			return default_handler(request, 403, 'Доступ к данной странице для вас запрещен')
		notification = Notification()
		notification.user = post.user
		notification.title = 'Проверка поста'
		if request.GET.get('is_available') == 'true':
			post.is_available = True
			notification.text = 'Ваш пост <a href="' + post.get_absolute_url() + '">' + post.title + '</a> был успешно проверен. Теперь он доступен и для других пользователей'
		elif request.GET.get('is_available') == 'false':
			post.is_available = False
			notification.text = 'Ваш пост <a href="' + post.get_absolute_url() + '">' + post.title + '</a> был заблокирован для других пользователей после проверки'
		post.save()
		notification.save()
		return redirect(reverse('posts:post', kwargs = {'pk': pk}))

class MyPostsView(AccessMixin, View):
	def get(self, request):
		checking = self.auth_check()
		if checking:
			return checking

		likes_count = 0
		views_count = 0
		comments_count = 0
		posts = Article.objects.filter(user = request.user)
		for post in posts:
			likes_count += post.likes
			views_count += post.views
			comments_count += post.comments.count()

		context = {
			'articles': posts.order_by('-date'),
			'likes_count': likes_count,
			'views_count': views_count,
			'comments_count': comments_count,
		}

		return render(request, 'posts/my.html', context)

class FavouritePostsView(AccessMixin, ListView):
	template_name = 'posts/favourite.html'
	context_object_name = 'articles'
	list_view = True

	def get_queryset(self):
		posts = FavouriteArticle.objects.filter(user = self.request.user)
		return posts

class NewPostView(AccessMixin, MessagesMixin, CreateView):
	template_name = 'posts/update.html'
	model = Article
	form_class = NewArticleForm
	success_url = reverse_lazy('posts:my')
	success_msg = 'Пост был успешно создал! Ожидайте модерациии'
	create_view = True

	def form_valid(self, form):
		self.object = form.save(commit = False)
		self.object.user = self.request.user
		self.object.save()
		notification = Notification()
		notification.user = User.objects.get(is_superuser = True)
		notification.title = 'Был создан новый пост'
		notification.text = self.object.user.username + ' создал новый пост - <a href="' + reverse('posts:post', args = [self.object.id]) + '">' + self.object.title + '</a>'
		notification.save()
		return super().form_valid(form)

	def get_context_data(self, **kwargs):
		kwargs['tags'] = Tag.objects.all()
		return super().get_context_data(**kwargs)

class UpdatePostView(AccessMixin, MessagesMixin, UpdateView):
	model = Article
	form_class = NewArticleForm
	template_name = 'posts/update.html'
	success_url = reverse_lazy('posts:my')
	update_view = True

	def get_context_data(self, **kwargs):
		kwargs['update'] = True
		kwargs['tags'] = Tag.objects.all()
		return super().get_context_data(**kwargs)

	def get_success_url(self):
		self.object.is_available = False
		self.object.save()
		self.set_success_msg('Пост был успешно обновлен! Ожидайте модерации')
		return self.success_url

class DeletePost(AccessMixin, MessagesMixin, DeleteView):
	success_msg = 'Ваш пост был успешно удален'
	model = Article
	success_url = reverse_lazy('posts:my')
	delete_view = True

	def get(self, request, *args, **kwargs):
		return default_handler(request, 400, 'Данная страница не поддерживает этот медот загрузки (get)')