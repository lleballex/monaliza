from django.contrib import messages
from django.shortcuts import render

class MessagesMixin:
	success_msg = None
	error_msg = None

	def get_success_url(self):
		if self.success_msg:
			messages.success(self.request, self.success_msg)
		if self.error_msg:
			messages.error(self.request, self.error_msg)

		if self.success_url:
			return self.success_url.format(**self.object.__dict__)
		else:
			raise ImproperlyConfigured("No URL to redirect to. Provide a success_url.")

	def set_success_msg(self, msg):
		messages.success(self.request, msg)

	def set_error_msg(self, msg):
		messages.error(self.request, msg)

class AccessMixin:
	message = 'К сожалению, эта страница не существует.'
	status_code = 404
	access_mixin = False

	def get_context_data(self, **kwargs):
		if self.access_mixin:
			kwargs = {'message': self.message, 'status_code': str(self.status_code),}
		return super().get_context_data(**kwargs)

	def get_template_names(self):
		if self.access_mixin:
			return ['access_mixin_wrapper.html']
		elif self.template_name is None:
			raise ImproperlyConfigured(
				"TemplateResponseMixin requires either a definition of "
				"'template_name' or an implementation of 'get_template_names()'")
		else:
			return [self.template_name]

	def mixin_render(self):
		return render(self.request, 'access_mixin_wrapper.html', {'message': self.message, 'status_code': str(self.status_code),})