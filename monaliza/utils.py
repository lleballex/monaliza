from django.shortcuts import render, redirect
from django.views.generic import View, UpdateView

def handler_404(request, exception):
	context = {
		'status_code': 404,
		'message': 'Кажется, здесь ничего нет, особенно гото, что вы ищете'
	}
	return render(request, 'handler.html', context)

def handler_500(request):
	context = {
		'status_code': 404,
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
	model = None
	info_404 = 'Кажется, тут ничего нет, особенно того, что вы ищете'
	error_url = None
	template_name = None
	object = None
	context_object_name = None
	success_func = None

	def get(self, request):
		id = request.GET.get('id')
		if not id:
			if self.error_url:
				return redirect(self.error_url)
			else:
				return default_handler(request, 404, self.info_404)
		try:
			self.object = self.model.objects.get(id = id)
		except self.model.DoesNotExist:
			return default_handler(request, 404, self.info_404)
		if self.success_func:
			self.success_func()
		return render(request, self.template_name, {self.context_object_name: self.object})

class UpdateMixin(UpdateView):
	model = None
	form_class = None
	template_name = None
	success_url = None
	new_kwargs = None
	info_404 = 'Кажется, тут ничего нет, особенно того, что вы ищете'

	def get(self, request, *args, **kwargs):
		id = self.request.GET.get('id')

		if not id:
			return default_handler(request, 404, self.info_404)
		if not request.user.is_authenticated:
			return default_handler(request, 401, 'Для доступа к этой странице необходимо авторизоваться')
		try:
			self.object = self.model.objects.get(id = id)
		except self.model.DoesNotExist:
			return default_handler(request, 404, self.info_404)
		if request.user != self.object.user:
			return default_handler(request, 403, 'Досуп к этой странице для вас запрещен')

		return super().get(request, *args, **kwargs)

	def get_object(self, queryset = None):
		id = self.request.GET.get('id')
		return self.model.objects.get(id = id)

	def get_context_data(self, **kwargs):
		if self.new_kwargs:
			for i in self.new_kwargs:
				kwargs[i] = self.new_kwargs[i] 
		return super().get_context_data(**kwargs)