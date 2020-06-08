from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, View, ListView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login
from django.http.response import HttpResponse
from django.http import Http404

from .forms import UserRegisterForm, UserLoginForm, UserUpdateForm
from .models import User, Notification, FavouriteArticle
from .utils import MessagesMixin, UserAccessMixin
from monaliza.utils import AccessViewMixin

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

	def get_success_url(self):
		return reverse_lazy('account:profile')

class UserLogout(LogoutView):
	next_page = reverse_lazy('posts:posts')

class ProfileView(AccessViewMixin, TemplateView):
	template_name = 'account/profile.html'
	template_view = True

class SettingsView(UserAccessMixin, MessagesMixin, UpdateView):
	form_class = UserUpdateForm
	template_name = 'account/update.html'
	success_url = reverse_lazy('account:settings')
	update_view = True

	def get_object(self, queryset = None):
		return User.objects.get(id = self.request.user.id)

	def form_invalid(self, form):
		for i in form.errors.values():
			for error in i:
				self.set_error_msg(error)
		new_form = UserUpdateForm(instance = self.get_object())
		return self.render_to_response(self.get_context_data(form = new_form))

	def form_valid(self, form):
		self.set_success_msg('Профиль был успешно обновлен!')
		self.object = form.save()
		return super().form_valid(form)


class NotificationsView(AccessViewMixin, ListView):
	template_name = 'account/notifications.html'
	context_object_name = 'notifications'
	list_view = True

	def get_queryset(self):
		return Notification.objects.filter(user = self.request.user).order_by('-date')

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