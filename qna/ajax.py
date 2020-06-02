from django.views.generic import View
from django.http import JsonResponse
from django.urls import reverse

from .models import Question, Answer

class AnswerSend(View):
	def get(self, request):
		question_id = request.GET.get('question_id')
		text = request.GET.get('text')

		if not question_id:
			return JsonResponse(status = 400, data = {'info': 'Id of the questions is None'})
		elif not text:
			return JsonResponse(status = 400, data = {'info': 'Text of the answer is None'})
		elif not request.user.is_authenticated:
			return JsonResponse(status = 401, data = {'info': 'User is not authenticated'})
		try:
			question = Question.objects.get(id = question_id)
		except Question.DoesNotExist:
			return JsonResponse(status = 404, data = {'info': 'Question with this id was not found'})

		answer = Answer()
		answer.user = request.user
		answer.question = question
		answer.text = text
		answer.save()
		html = '''
				<li id="answer-%i">
				<img src="static/account/images/user_2.png">
				<div class="answer">
				<div class="user">
				<div>
				<div>%s</div>
				<div class="date">%s</div>
				</div>
				<div>
				''' % (answer.id, answer.user.username, answer.date)
		if request.user == question.user:
			html += '''<i class="fa fa-check" onclick="answer_right('%s', %i, false)"></i>''' % (reverse('qna:answer_right'), answer.id)
		html += '''
				<i class="fa fa-times" onclick="answer_delete('%s', %i)" style="padding-left: 5px;"></i>
				</div></div>
				<div class="text">%s</div>
				</div></li>
				''' % (reverse('qna:answer_delete'), answer.id, answer.text)
		return JsonResponse({'html': html})

class AnswerDelete(View):
	def get(self, request):
		id = request.GET.get('id')

		if not id:
			return JsonResponse(status = 400, data = {'info': 'Id of the answer is None'})
		elif not request.user.is_authenticated:
			return JsonResponse(status = 401, data = {'info': 'User is not authenticated'})
		try:
			answer = Answer.objects.get(id = id)
		except Answer.DoesNotExist:
			return JsonResponse(status = 404, data = {'info': 'Answer with this id was not found'})
		if request.user != answer.user:
			return JsonResponse(status = 403, data = {'info': 'Active user is not user of the answer'}) 

		if answer.is_right_answer:
			answer.question.is_solved = False
			answer.question.save()
		answer.delete()
		return JsonResponse({})

class AnswerRight(View):
	def get(self, request):
		id = request.GET.get('id')

		if not id:
			return JsonResponse(status = 400, data = {'info': 'Id of the answer is None'})
		elif not request.user.is_authenticated:
			return JsonResponse(status = 401, data = {'info': 'User is not authenticated'})
		try:
			answer = Answer.objects.get(id = id)
		except Answer.DoesNotExist:
			return JsonResponse(status = 404, data = {'info': 'Answer with this id was not found'})
		if request.user != answer.user:
			return JsonResponse(status = 403, data = {'info': 'Active user is not user of the answer'}) 

		if answer.is_right_answer:
			answer.is_right_answer = False
			answer.question.is_solved = False
		else: 
			for i in Answer.objects.filter(question = answer.question):
				i.is_right_answer = False
				i.save()
			answer.is_right_answer = True
			answer.question.is_solved = True

		answer.save()
		answer.question.save()
		return JsonResponse({})