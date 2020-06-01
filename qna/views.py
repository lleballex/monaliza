from django.shortcuts import render, redirect
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.http.response import HttpResponse

from .models import Question, Answer, Tag
from .forms import QuestionForm
from account.models import User, Notification
from account.utils import MessagesMixin

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

	def get_template_names(self):
		self.object.views += 1
		self.object.save()
		return [self.template_name]

class SetAnswer(View):
	def get(self, request, pk):
		question = Question.objects.get(id = pk)
		answer = Answer()
		answer.user = request.user
		answer.question = question
		answer.text = request.GET.get('text')
		answer.save()
		'''if answer.user == question.user and not question.is_solved:
			question.is_solved = True
			question.save()
			answer.is_right_answer = True
			answer.save()'''
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
		question.is_solved = True
		question.save()
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
		questions_count = 0
		views_count = 0
		answers_count = 0
		for question in questions:
			questions_count += 1
			views_count += question.views
			answers_count += question.answers.count()
		content = {
			'questions': questions,
			'questions_count': questions_count,
			'views_count': views_count,
			'answers_count': answers_count,
		}
		return render(request, 'qna/my_questions.html', content)

class NewQuestionView(CreateView):
	model = Question
	form_class = QuestionForm
	template_name = 'qna/update.html'
	success_url = reverse_lazy('qna:all_questions')

	def form_valid(self, form):
		self.object = form.save(commit = False)
		self.object.user = self.request.user
		#self.object.text = self.post_text(self.object.text)
		self.object.save()
		notification = Notification()
		notification.user = User.objects.get(is_superuser = True)
		notification.title = 'Был задан новый вопрос'
		notification.text = self.object.user.username + ' задал вопрос - <a href="' + self.object.title + '">' + self.object.title + '</a>'
		notification.save()
		return super().form_valid(form)

	def get_context_data(self, **kwargs):
		kwargs['tags'] = Tag.objects.all()
		return super().get_context_data(**kwargs)

class QuestionUpdateView(UpdateView):
	model = Question
	form_class = QuestionForm
	template_name = 'qna/update.html'
	success_url = reverse_lazy('qna:my_questions')

	def get_context_data(self, **kwargs):
		kwargs['update'] = True
		return super().get_context_data(**kwargs)

class QuestionDelete(MessagesMixin, DeleteView):
	model = Question
	success_url = reverse_lazy('qna:my_questions')
	success_msg = 'Ваш вопрос был успешно удален'

class MyAnswersView(View):
	def get(self, request):
		answers = Answer.objects.filter(user = request.user)
		answers_count = 0
		right_answers_count = 0
		for answer in answers:
			answers_count += 1
			if answer.is_right_answer:
				right_answers_count += 1
		content = {
			'answers': answers,
			'answers_count': answers_count,
			'right_answers_count': right_answers_count,
		}
		return render(request, 'qna/my_answers.html', content)

class UpdateAnswerView(View):
	def get(self, request, pk):
		answer = Answer.objects.get(id = pk)
		context = {
			'answer': answer,
			'question': answer.question,
			'update': True,
		}
		return render(request, 'qna/detail.html', context)

	def post(self, request, pk):
		answer = Answer.objects.get(id = pk)
		answer.text = request.POST.get('answer-text')
		answer.save()
		return redirect(reverse('qna:my_answers'))

class DeleteAnswerView(DeleteView):
	model = Answer
	success_url = reverse_lazy('qna:my_answers')
	success_msg = 'Ваш ответ был успешно удален'