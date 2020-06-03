from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StartPageIndexSitemap(Sitemap):
	changefreq = 'daily'
	priority = 0.9

	def items(self):
		return ['start_page:main_view']

	def location(self, item):
		return reverse(item)