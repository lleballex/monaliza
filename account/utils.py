from django.contrib import messages
from django.shortcuts import render

from monaliza.utils import AccessMixin

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

class UserAccessMixin(AccessMixin):
	update_view = False

	def get(self, request, *args, **kwargs):
		if self.update_view:
			checking = self.auth_check()
			if checking:
				return checking
			self.object = self.get_object()
			return super().get(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		if self.update_view:
			checking = self.auth_check()
			if checking:
				return checking
			self.object = self.get_object()
			return super().post(request, *args, **kwargs)
