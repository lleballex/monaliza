from django.shortcuts import render, redirect
from django.views.generic import CreateView, View, UpdateView, ListView, DeleteView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login

from .forms import *
from .models import User, Notification, FavouriteArticle
from it_articles.models import Article
from .utils import *

class UserRegisterView(CreateView):
	model = User
	form_class = UserRegisterForm
	template_name = 'account/register.html'
	success_url = reverse_lazy('account:profile')

	def form_valid(self, form):
		form_valid = super().form_valid(form)
		username = form.cleaned_data['username']
		password = form.cleaned_data['password1']
		auth_user = authenticate(username = username, password = password)
		login(self.request, auth_user)
		return form_valid

class UserLoginView(LoginView):
	template_name = 'account/login.html'
	form_class = UserLoginForm
	success_url = reverse_lazy('start_page:main_view')

	def get_success_url(self):
		return reverse_lazy('it_articles:articles_all')

class ProfileView(View):
	def get(self, request):
		context = {
			'articles': Article.objects.filter(user = request.user).order_by('-date'),
		}
		return render(request, 'account/profile.html', context)

class MyArticlesView(MessagesMixin, View):
	def get(self, request):
		#self.set_success_msg('qwertyu')
		#self.set_success_msg('sdfsdfsdf')
		#self.set_error_msg('sdf')
		likes = 0
		all_articles = 0
		articles = Article.objects.filter(user = request.user)
		for article in articles:
			likes += article.likes
			all_articles += 1

		context = {
			'articles': articles.order_by('-id'),
			'likes': likes,
			'all_articles': all_articles,
		}

		return render(request, 'account/my_articles.html', context)

class SettingsView(MessagesMixin, View):
	def get(self, request):
		context = {
			'form': UserUpdateForm(instance = request.user), 
		}
		return render(request, 'account/update.html', context)

	def post(self, request):
		right_username = request.user.username
		right_email = request.user.email
		form = UserUpdateForm(request.POST, request.FILES, instance = request.user)
		if form.is_valid():
			form.save()
			self.set_success_msg('Profile was successfule updated')
		else:
			username = request.POST.get('username')
			email = request.POST.get('email')
			form = UserUpdateForm(instance = request.user)
			for user in User.objects.all():
				if username == user.username and user.email != right_email:
					self.set_error_msg('This username is already taken')
				if email == user.email and user.username != right_username:
					print(user, ' - ', user.email)
					print(right_username)
					self.set_error_msg('This email is alreade taken')
		return redirect(reverse('account:settings'))

class NewArticleView(MessagesMixin, CreateView):
	template_name = 'account/edit_article.html'
	model = Article
	form_class = NewArticleForm
	success_url = reverse_lazy('account:my_articles')
	success_msg = 'The article was successfuly created. Please wait for verification'

	def form_valid(self, form):
		self.object = form.save(commit = False)
		self.object.user = self.request.user
		self.object.save()
		return super().form_valid(form)

class EditArticleView(MessagesMixin, UpdateView):
	model = Article
	form_class = NewArticleForm
	template_name = 'account/edit_article.html'
	success_url = reverse_lazy('account:my_articles')
	success_msg = 'The article was successfuly updated'

	def get_context_data(self, **kwargs):
		kwargs['update'] = True
		return super().get_context_data(**kwargs)

class DeleteArticleView(MessagesMixin, DeleteView):
	success_msg = 'The article was successfuly deleted'
	model = Article
	success_url = reverse_lazy('account:my_articles')

class NotificationsView(View):
	def get(self, request):
		print('f')
		context = {
			'notifications': Notification.objects.filter(user = request.user)
		}
		return render(request, 'account/notifications.html', context)

class FavouriteView(View):
	def get(self, request):
		context = {
			'articles': FavouriteArticle.objects.filter(user = request.user),
		}
		return render(request, 'account/favourite.html', context)