from django.shortcuts import render, redirect
from django.views.generic import View, UpdateView

def handler_404(request, exception = None):
	context = {
		'status_code': 404,
		'message': 'Кажется, здесь ничего нет, особенно гото, что вы ищете'
	}
	return render(request, 'handler.html', context)

def handler_500(request):
	context = {
		'status_code': 500,
		'message': 'С сервером какие-то проблемы, но мы скоро все починим'
	}
	return render(request, 'handler.html', context)

def default_handler(request, status_code, info): 
	context = {
		'status_code': status_code,
		'message': info,
	}
	response = render(request, 'handler.html', context)
	return response


class DetailMixin(View):
	auth_check = False

	def get(self, request, *args, **kwargs):
		if self.auth_check:
			if not request.user.is_authenticated:
				return default_handler(request, 401, 'Для доступа к этой странице необходимо авторизоваться')


		self.object = self.get_object()
		context = self.get_context_data(object = self.object)
		return self.render_to_response(context)

class AccessMixin(View):
	list_view = False
	update_view = False
	create_view = False
	delete_view = False

	def auth_check(self):
		if not self.request.user.is_authenticated:
			return default_handler(self.request, 401, 'Для доступа к этой странице необходимо авторизоваться')
		else:
			return False

	def user_check(self):
		if self.request.user != self.object.user and not self.request.user.is_superuser:
			return default_handler(self.request, 403, 'Доступ к этой странице для вас запрещен')
		else:
			return False

	def multi_check(self):
		auth_checking = self.auth_check()
		if auth_checking:
			return auth_checking

		user_checking = self.user_check()
		if user_checking:
			return user_checking

		return False

	def get(self, request, *args, **kwargs):
		if self.list_view:
			checking = self.auth_check()
			if checking:
				return checking
			self.object_list = self.get_queryset()
			context = self.get_context_data()
			return self.render_to_response(context)

		elif self.update_view:
			self.object = self.get_object()
			checking = self.multi_check()
			if checking:
				return checking
			return super().get(request, *args, **kwargs)

		elif self.create_view:
			self.object = None
			checking = self.auth_check()
			if checking:
				return checking
			return super().get(request, *args, **kwargs)

		elif self.delete_view:
			return default_handler(request, 400, 'Эта страница не поддерживает этот метод запроса (get)')


	def post(self, request, *args, **kwargs):
		if self.list_view:
			return default_handler(request, 400, 'Эта страница не поддерживает этот метод запроса (get)')

		elif self.update_view:
			self.object = self.get_object()
			checking = self.multi_check()
			if checking:
				return checking
			return super().post(request, *args, **kwargs)

		elif self.create_view:
			self.object = None
			checking = self.auth_check()
			if checking:
				return checking
			return super().post(request, *args, **kwargs)

		elif self.delete_view:
			self.object = self.get_object()
			checking = self.multi_check()
			if checking:
				return checking
			self.object.delete()
			return redirect(self.get_success_url())