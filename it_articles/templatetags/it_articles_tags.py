from django import template
from ..models import Article
from account.models import FavouriteArticle

register = template.Library()

@register.simple_tag
def is_liked(user, article):
	try:
		fav_article = article.favourite_articles.get(user = user)
		return 'is_liked'
	except:
		return ''
	'''if fav_article in user.favourite_articles.all():
		return 'is_liked'
	else:
		return '''

@register.simple_tag
def is_liked_fa(user, article):
	try:
		fav_article = article.favourite_articles.get(user = user)
		return 'fa-thumbs-up'
	except:
		return 'fa-thumbs-o-up'

@register.simple_tag
def is_liked_fa_heart(user, article):
	try:
		fav_article = article.favourite_articles.get(user = user)
		return 'fa-heart'
	except:
		return 'fa-heart-o'