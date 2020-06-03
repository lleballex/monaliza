from django.shortcuts import render, redirect
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy

from .models import Question, Answer, Tag
from .forms import QuestionForm
from account.models import User, Notification
from monaliza.utils import default_handler

class Index(View):
	def get(self, request):
		return redirect(reverse('qna:questions'))

class QuestionsView(ListView):
	queryset = Question.objects.order_by('-date')
	template_name = 'qna/questions.html'
	context_object_name = 'questions'

class QuestionView(DetailView):
	model = Question
	template_name = 'qna/question.html'
	context_object_name = 'question'
	
	def get_context_data(self, **kwargs):
		self.object.views += 1
		self.object.save()
		return super().get_context_data(**kwargs)

class UpdateQuestionView(UpdateView):
	model = Question
	form_class = QuestionForm
	template_name = 'qna/question_update.html'
	success_url = reverse_lazy('qna:questions_my')
	
	def get_context_data(self, **kwargs):
		kwargs['update'] = True
		return super().get_context_data(**kwargs)

class MyQuestionsView(ListView):
	template_name = 'qna/questions_my.html'
	context_object_name = 'questions'

	def get_queryset(self):
		return Question.objects.filter(user = self.request.user).order_by('-date')

	def get_context_data(self, **kwargs):
		views_count = 0
		answers_count = 0
		for obj  in self.object_list:
			views_count += obj.views
			answers_count += obj.answers.count()
		kwargs['views_count'] = views_count
		kwargs['answers_count'] = answers_count
		return super().get_context_data(**kwargs)

class NewQuestionView(CreateView):
	model = Question
	form_class = QuestionForm
	template_name = 'qna/question_update.html'
	success_url = reverse_lazy('qna:questions')

	def form_valid(self, form):
		self.object = form.save(commit = False)
		self.object.user = self.request.user
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

class DeleteQuestion(DeleteView):
	model = Question
	success_url = reverse_lazy('qna:questions_my')

class MyAnswersView(ListView):
	template_name = 'qna/answers_my.html'
	context_object_name = 'answers'

	def get_queryset(self):
		return Answer.objects.filter(user = self.request.user).order_by('-date')

	def get_context_data(self, **kwargs):
		right_answers_count = 0
		for obj in self.object_list:
			if obj.is_right_answer:
				right_answers_count += 1
		kwargs['right_answers_count'] = right_answers_count
		return super().get_context_data(**kwargs)

class UpdateAnswerView(View):
	def get(self, request, pk):
		answer = Answer.objects.get(id = pk)
		context = {
			'answer': answer,
			'question': answer.question,
			'update': True,
		}
		return render(request, 'qna/question.html', context)

	def post(self, request, pk):
		answer = Answer.objects.get(id = pk)
		answer.text = request.POST.get('answer-text')
		answer.save()
		return redirect(reverse('qna:answers_my'))

class DeleteAnswer(View):
	def get(self, request, *args, **kwargs):
		return default_handler(request, 405, 'Эта страница не подразумевает такой метод (get)')

	def post(self, request, pk):
		try:
			self.object = Answer.objects.get(id = pk)
		except Answer.DoesNotExist:
			return default_handler(request, 404, 'Такого вопроса не существует')
		if request.user != self.object.user:
			return default_handler(request, 401, 'Доступ к этой странице для вас запрещен')
		self.object.delete()
		return redirect(reverse_lazy('qna:answers_my'))