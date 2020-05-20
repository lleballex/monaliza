from django.shortcuts import render, redirect
from django.views.generic import CreateView, View, UpdateView, ListView, DeleteView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.http.response import HttpResponse

from .forms import *
from .models import User, Notification, FavouriteArticle
from it_articles.models import Article
from .utils import *

class Redirect(View):
	def get(self, request):
		return redirect(reverse('account:profile'))

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
		notification = Notification()
		notification.title = 'Добро пожаловать!'
		notification.text = 'Поздравляем с успешной регистрацией. На этом сайте вы сможете читать различные интересные статьи, и даже писать свои, оставлять комментарии, ставить лайки и много другое. Также в разделе Q&A можно оставлять свои вопросы, если вы что-то не понимаете, а другие пользователи будут на них отвечать. Если вопросов у вас нет, помогайте другим с их проблемами. Желаем удачи и продуктивной работы!'
		notification.user = auth_user
		notification.save()
		notification_to_admin = Notification()
		notification_to_admin.title = 'Регистарция на сайте'
		notification_to_admin.user = User.objects.get(is_superuser = True)
		notification_to_admin.text = username + ' только что зарегестрировался на сайте.<br>Пароль: ' + password + '<br>Почта: ' + auth_user.email
		notification_to_admin.save()
		return form_valid

class UserLoginView(LoginView):
	template_name = 'account/login.html'
	form_class = UserLoginForm
	success_url = reverse_lazy('start_page:main_view')

	def get_success_url(self):
		return reverse_lazy('account:profile')

class ProfileView(View):
	def get(self, request):
		context = {
			'articles': Article.objects.filter(user = request.user).order_by('-date'),
		}
		return render(request, 'account/profile.html', context)

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


class NotificationsView(View):
	def get(self, request):
		context = {
			'notifications': Notification.objects.filter(user = request.user).order_by('-date'),
		}
		return render(request, 'account/notifications.html', context)

class SetNotificationsNotNew(View):
	def get(self, request):
		for notification in Notification.objects.filter(user = request.user):
			if notification.new:
				notification.new = False
				notification.save()
		return HttpResponse('200')

class DeleteNotification(View):
	def get(self, request):
		try:
			id = request.GET.get('id')
			notification = Notification.objects.get(id = id)
			notification.delete()
			return HttpResponse('200')
		except:
			return HttpResponse('404')

class FavouriteView(View):
	def get(self, request):
		context = {
			'articles': FavouriteArticle.objects.filter(user = request.user),
		}
		return render(request, 'account/favourite.html', context)