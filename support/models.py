from django.db import models

from account.models import User

class Ticket(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'tickets')
	title = models.CharField(max_length = 1000)
	text = models.TextField()