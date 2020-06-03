from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Article

class PostsSitemap(Sitemap):
	changefreq = 'daily'
	priority = 0.9

	def items(self):
		return Article.objects.filter(is_available = True)

	def location(self, item):
		return reverse('posts:detail', kwargs = {'pk': item.id})

class PostsIndexSitemap(Sitemap):
	changefreq = 'daily'
	priority = 0.9

	def items(self):
		return['posts:all']

	def location(self, item):
		return reverse(item)