from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
	def create_user(self, username, email, password):
		if not email:
			raise ValueError('User must have an email address')
		if not username:
			raise ValueError('User must have a username')
		user = self.model(username = username, email = self.normalize_email(email))
		user.set_password(password)
		user.save(using = self._db)
		return user

	def create_superuser(self, username, email, password):
		user = self.create_user(username = username, email = email, password = password)
		user.is_staff = True
		user.is_admin = True
		user.is_superuser = True
		user.save(using = self._db)
		return user

class User(AbstractBaseUser):
	GENDER = [
		('male', 'MALE'),
		('female', 'FEMALE'),
	]

	username = models.CharField('username', max_length = 30, unique = True)
	email = models.EmailField('email adress', max_length = 60, unique = True)
	first_name = models.CharField('first name', max_length = 30, null = True, blank = True)
	last_name = models.CharField('last name', max_length = 30, null = True, blank = True)
	date_joined = models.DateField('date of join', auto_now_add = True)
	age = models.IntegerField('age', null = True, blank = True)
	gender = models.CharField('gender', max_length = 30, choices = GENDER, null = True, blank = True)
	image = models.ImageField(upload_to = 'account/avatars/%y/%m/%d', null = True, blank = True)
	is_staff = models.BooleanField(default = False)
	is_admin = models.BooleanField(default = False)
	is_superuser = models.BooleanField(default = False)
	is_active = models.BooleanField(default = True)

	objects = UserManager()

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']

	def __str__(self):
		return self.username

	def has_perm(self, perm, obj = None):
		return self.is_admin

	def has_module_perms(self, app_label):
		return True

	def get_absolute_url(self):
		return '/account/profiles/%i/' % self.id

	def get_favourites_articles(self):
		return self.favourite_articles.all

class Notification(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'notifications')
	title = models.CharField(max_length = 300)
	text = models.CharField(max_length = 1000)
	date = models.DateTimeField(auto_now = True)
	new = models.BooleanField(default = True)

	def get_absolute_url(self):
		return '/notifications/' + str(self.id) + '/'

from it_articles.models import Article
class FavouriteArticle(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'favourite_articles')
	article = models.ForeignKey(Article, on_delete = models.CASCADE, related_name = 'favourite_articles')
	date = models.DateTimeField(auto_now = True)