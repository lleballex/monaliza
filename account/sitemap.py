from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import User, Notification

class AccountIndexSitemap(Sitemap):
	changefreq = 'daily'
	priority = 0.9

	def items(self):
		return ['account:login', 'account:register', 'account:profile', 'account:settings', 'account:my_articles']

	def location(self, item):
		return reverse(item)

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