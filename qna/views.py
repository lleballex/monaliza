from django.shortcuts import render, redirect
from django.views.generic import View, ListView, DetailView, CreateView
from django.urls import reverse, reverse_lazy
from django.http.response import HttpResponse

from .models import Question, Answer
from .forms import QuestionForm
from account.models import User

class Redirect(View):
	def get(self, request):
		return redirect(reverse('qna:all_questions'))

class AllQuestionsView(ListView):
	queryset = Question.objects.order_by('-date')
	template_name = 'qna/all_questions.html'
	context_object_name = 'questions'

class DetailQuestionView(DetailView):
	model = Question
	template_name = 'qna/detail.html'
	context_object_name = 'question'

class SetAnswer(View):
	def get(self, request, pk):
		answer = Answer()
		answer.user = request.user
		answer.question = Question.objects.get(id = pk)
		answer.text = request.GET.get('text')
		answer.save()
		return HttpResponse('200')

class DeleteAnswer(View):
	def get(self, request, pk):
		answer = Answer.objects.get(id = request.GET.get('id'))
		answer.delete()
		return HttpResponse('200')

class SetRightAnswer(View):
	def get(self, request, pk):
		question = Question.objects.get(id = pk)
		for answer in question.answers.all():
			if answer.is_right_answer:
				answer.is_right_answer = False
				answer.save()
		right_answer = Answer.objects.get(id = request.GET.get('id'))
		right_answer.is_right_answer = True
		right_answer.save()
		return HttpResponse('200')

class DeleteRightAnswer(View):
	def get(self, request, pk):
		answer = Answer.objects.get(id = request.GET.get('id'), is_right_answer = True)
		answer.is_right_answer = False
		answer.save()
		return HttpResponse('200')

class MyQuestionsView(View):
	def get(self, request):
		questions = Question.objects.filter(user = request.user)
		content = {
			'questions': questions,
		}
		return render(request, 'qna/my_questions.html', content)

class NewQuestionView(CreateView):
	model = Question
	form_class = QuestionForm
	template_name = 'qna/update.html'
	success_url = reverse_lazy('qna:all_questions')