from django.contrib.sitemaps import Sitemap
from .models import User, Notification

class UserSitemap(Sitemap):
	changefreq = 'weekly'
	priority = 0.9

	def items(self):
		return User.objects.all()

	def lastmod(self, obj):
		return obj.date_joined

class NotificationSitemap(Sitemap):
	changefreq = 'weekly'
	priority = 0.9

	def items(self):
		return Notification.objects.all()