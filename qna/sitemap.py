from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Question, Answer

class QuestionsSitemap(Sitemap):
	changefreq = 'daily'
	priority = 0.8

	def items(self):
		return Question.objects.all()

	def location(self, item):
		return reverse('qna:detail', kwargs = {'pk': item.id})

class AnswersSitemap(Sitemap):
	changefreq = 'daily'
	priority = 0.8

	def items(self):
		return Answer.objects.all()

	def location(self, item):
		return reverse('qna:detail', kwargs = {'pk': item.question.id})