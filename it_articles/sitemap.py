from django.contrib.sitemaps import Sitemap

from .models import Article

class ArticlesSitemap(Sitemap):
	changefreq = 'weekly'
	priority = 0.9

	def items(self):
		return Article.objects.filter(is_available = True)