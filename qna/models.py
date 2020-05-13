from django.db import models

from account.models import User

class Question(models.Model):
	title = models.CharField(max_length = 1000)
	text = models.TextField()
	date = models.DateTimeField(auto_now_add = True)
	user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'questions')
	is_solved = models.BooleanField(default = False)

class Answer(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'answers')
	question = models.ForeignKey(Question, on_delete = models.CASCADE, related_name = 'answers')
	text = models.TextField()
	date = models.DateTimeField(auto_now_add = True)
	is_right_answer = models.BooleanField(default = False)