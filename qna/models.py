from django.db import models

from account.models import User

TAGS = [
	('CPP', 'c++'),
	('PYTHON', 'python'),
	('WEB', 'web')
]

class Question(models.Model):
	title = models.CharField(max_length = 1000)
	text = models.TextField()
	date = models.DateTimeField(auto_now_add = True)
	views = models.IntegerField(default = 0)
	user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'questions')
	is_solved = models.BooleanField(default = False)
	tags = models.CharField(max_length = 100, null = True, blank = True)
	
class Answer(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'answers')
	question = models.ForeignKey(Question, on_delete = models.CASCADE, related_name = 'answers')
	text = models.TextField()
	date = models.DateTimeField(auto_now_add = True)
	is_right_answer = models.BooleanField(default = False)