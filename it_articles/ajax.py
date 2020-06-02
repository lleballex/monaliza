from django.views.generic import View
from django.http import JsonResponse

from .models import Article, Comment
from account.models import FavouriteArticle

class CommentSend(View):
	def get(self, request):
		text = request.GET.get('text')
		post_id = request.GET.get('post_id')

		if not text:
			return JsonResponse(status = 400, data = {'info': 'Text of the comment is none'})
		if not post_id:
			return JsonResponse(status = 400, data = {'info': 'Id of the post is none'})
		if not request.user.is_authenticated:
			return JsonResponse(status = 400, data = {'info': 'User is not authenticated'})
		try:
			article = Article.objects.get(id = post_id)
		except Article.DoesNotExist:
			return JsonResponse(status = 404, data = {'info': 'Post with this id was not found'})
		
		comment = Comment()
		comment.user = request.user
		comment.text = text
		comment.article = article
		comment.save()
		data = {
			'text': comment.text,
			'date': comment.date.strftime('%B %d, %H:%M'),
			'id': comment.id,
		}
		return JsonResponse(data)

class CommentDelete(View):
	def get(self, request):
		id = request.GET.get('id')

		if not id:
			return JsonResponse(status = 400, data = {'info': 'Id of the comment is none'})
		if not request.user.is_authenticated:
			return JsonResponse(status = 401, data = {'info': 'User is not authenticated'})
		try:
			comment = Comment.objects.get(id = id)
		except Comment.DoesNotExist:
			return JsonResponse(status = 404, data = {'info': 'Comment with this id was not found'})
		if comment.user != request.user:
			return JsonResponse(status = 403, data = {'info': 'Active user is not user of the comment'})

		comment.delete()
		return JsonResponse({})

class PostLike(View):
	def get(self, request):
		id = request.GET.get('id')

		if not id:
			return JsonResponse(status = 400, data = {'info': 'Id of the post is none'})
		if not request.user.is_authenticated:
			return JsonResponse(status = 401, data = {'info': 'User is not authenticated'})
		try:
			post = Article.objects.get(id = id)
		except Article.DoesNotExist:
			return JsonResponse(status = 404, data = {'info': 'Post with this id was not found'})
		
		try:	
			fav_post = FavouriteArticle.objects.get(article = post, user = request.user)
			fav_post.delete()
			post.likes -= 1
			post.save()
			return JsonResponse({'created': False, 'deleted': True})
		except FavouriteArticle.DoesNotExist:
			fav_post = FavouriteArticle()
			fav_post.article = post
			fav_post.user = request.user
			fav_post.save()
			post.likes += 1
			post.save()
			return JsonResponse({'created': True, 'deleted': False})