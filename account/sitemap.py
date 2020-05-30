from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import User, Notification

class AccountIndexSitemap(Sitemap):
	changefreq = 'weekly'
	priority = 0.9

	def items(self):
		return ['account:login', 'account:register']

	def location(self, item):
		return reverse(item)

class UserSitemap(Sitemap):
	changefreq = 'daily'
	priority = 0.9

	def items(self):
		return User.objects.all()

	def location(self, item):
		return reverse('search:user_page', kwargs = {'username': item.username})