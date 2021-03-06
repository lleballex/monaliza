from django.db import models
from account.models import User

class Article(models.Model):
	LANGUAGE = [
		('cpp', 'C++'),
		('python', 'PYTHON'),
		('web', 'WEB'),
	]

	title = models.CharField(max_length = 100)
	text = models.TextField()
	user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'articles')
	date = models.DateTimeField(auto_now_add = True)
	likes = models.IntegerField(default = 0)
	views = models.IntegerField(default = 0)
	is_available = models.BooleanField(default = False)
	tags = models.CharField(max_length = 100, null = True, blank = True)
	
	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return '/posts/detail/%i' % self.id

class Comment(models.Model):
	article = models.ForeignKey(Article, on_delete = models.CASCADE, related_name = 'comments')
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	text = models.CharField(max_length = 1000)
	date = models.DateTimeField(auto_now = True)
	likes = models.IntegerField(default = 0)

	def __str__(self):
		return self.user.username

	def qwert(self):
		print('hello')
		self.text = 'hello world'
		return self.date