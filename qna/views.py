from django.shortcuts import render, redirect
from django.views.generic import View, ListView
from django.urls import reverse

from .models import Question, Answer

def redirect_to_questions(request):
	return redirect(reverse('qna:all_questions'))

class AllQuestionsView(ListView):
	queryset = Question.objects.order_by('-date')
	template_name = 'qna/all_questions.html'
	context_object_name = 'questions'

