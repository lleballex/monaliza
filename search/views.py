from django.shortcuts import render
from django.views.generic import View
from django.http import Http404

from it_articles.models import Article
from qna.models import Question
from account.models import User

class SearchView(View):
	def get(self, request):
		text = request.GET.get('text')
		model = request.GET.get('model')
		sort = request.GET.get('sort')
		template_name = 'search/search_result.html'

		context = {'articles': None, 'questions': None, 'users': None, 'model': model,}

		if model == 'post':
			if sort == 'time':
				context['articles'] = Article.objects.filter(title__icontains = text, is_available = True).order_by('-date')
			elif sort == 'likes':
				context['articles'] = Article.objects.filter(title__icontains = text, is_available = True).order_by('-date').order_by('-likes') 
			elif sort == 'views':
				context['articles'] = Article.objects.filter(title__icontains = text, is_available = True).order_by('-date').order_by('-views')
		elif model == 'question':
			context['questions'] = Question.objects.filter(title__icontains = text).order_by('-date')
		elif model == 'user':
			#if sort == 'time':
			context['users'] = User.objects.filter(username__icontains = text)
			#else:
			#	#context['articles'] = User.objects.filter(username_contains = text).order_by('-likes') 

		return render(request, template_name, context)

class UserView(View):
	def get(self, request, username):
		try:
			user = User.objects.get(username = username)
		except User.DoesNotExist:
			raise Http404
		context = {'user': user}
		return render(request, 'search/user_page.html', context)
		