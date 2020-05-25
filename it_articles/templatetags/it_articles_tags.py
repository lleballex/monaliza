from django import template
from math import ceil, floor

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

def get_menu(objects_count, page):
	on_page = 10
	#objects_count = Article.objects.all().count()
	objects_count = int(objects_count)
	menu = []
	menu_count = 9
	menu_max = ceil(objects_count / on_page)
	menu_bottom = ceil(menu_count / 2)
	page = int(page)

	if menu_max < menu_count:
		menu_count = menu_max
		menu_bottom = ceil(menu_count / 2)

	if page > menu_max - menu_bottom:
		for i in range(menu_max - menu_count + 1, menu_max + 1):
			menu.append(str(i))
	elif page >= menu_bottom:
		for i in range(page - menu_bottom + 1, page + menu_bottom + 1):
			menu.append(str(i))
	else:
		for i in range(1, menu_count + 1):
			menu.append(str(i))

	return menu

register.filter('get_menu', get_menu)

def without_html(text):
	new_text = ''
	tag = False
	for i in text:
		if i == '<' and not tag:
			tag = True
		if not tag:
			new_text += i
		elif i == '>' and tag:
			tag = False

	return new_text

register.filter('without_html', without_html)

