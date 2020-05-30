from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Article

class ArticlesSitemap(Sitemap):
	changefreq = 'daily'
	priority = 0.8

	def items(self):
		return Article.objects.filter(is_available = True)

class ItArticlesIndexSitemap(Sitemap):
	changefreq = 'daily'
	priority = 0.9

	def items(self):
		return['posts:all_posts', 'start_page:main_view']

	def location(self, item):
		return reverse(item)