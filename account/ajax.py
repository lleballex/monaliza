from django.views.generic import View
from django.http import JsonResponse

from account.models import Notification

class NotificationsNew(View):
	def get(self, request):
		if not request.user.is_authenticated:
			return JsonResponse(status = 401, data = {'info': 'User is not authenticated'})

		for notification in request.user.notifications.all():
			if notification.new:
				notification.new = False
				notification.save()

		return JsonResponse({})

class NotificationDelete(View):
	def get(self, request):
		id = request.GET.get('id')

		if not id:
			return JsonResponse(status = 400, data = {'info': 'Id of the notification is None'})
		if not request.user.is_authenticated:
			return JsonResponse(status = 401, data = {'info': 'User is not authenticated'})
		try:
			notification = Notification.objects.get(id = id)
		except Notification.DoesNotExist:
			return JsonResponse(status = 400, data = {'info': 'Notification with this id was not found'})
		if notification.user != request.user:
			return JsonResponse(status = 403, data = {'info': 'Active user is not user of the notification'})

		notification.delete()
		return JsonResponse({})		
