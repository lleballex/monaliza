from django.shortcuts import render
from django.views.generic import View

from it_articles.models import Article
from account.models import User

class SearchView(View):
	def get(self, request):
		text = request.GET.get('text')
		model = request.GET.get('model')
		sort = request.GET.get('sort')
		template_name = 'search/search_result.html'

		context = {'articles': None, 'model': model,}

		if model == 'post':
			if sort == 'time':
				context['articles'] = Article.objects.filter(title__contains = text).order_by('-date')
			elif sort == 'likes':
				context['articles'] = Article.objects.filter(title__contains = text).order_by('-date').order_by('-likes') 
			elif sort == 'views':
				context['articles'] = Article.objects.filter(title__contains = text).order_by('-date').order_by('-views')
		elif model == 'user':
			#if sort == 'time':
			context['users'] = User.objects.filter(username__contains = text)
			#else:
			#	#context['articles'] = User.objects.filter(username_contains = text).order_by('-likes') 

		return render(request, template_name, context)

class UserView(View):
	def get(self, request, username):
		try:
			user = User.objects.get(username = username)
			context = {'user': user}
			return render(request, 'search/user_page.html', context)
		except:
			return render(request, 'wrapper.html')