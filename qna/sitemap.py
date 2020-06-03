from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Question

class QuestionsSitemap(Sitemap):
	changefreq = 'daily'
	priority = 0.9

	def items(self):
		return Question.objects.all()

	def location(self, item):
		return reverse('qna:question', kwargs = {'pk': item.id})