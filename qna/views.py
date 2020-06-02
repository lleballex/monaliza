from django.shortcuts import render, redirect
from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy

from .models import Question, Answer, Tag
from .forms import QuestionForm
from account.models import User, Notification
from account.utils import MessagesMixin
from monaliza.utils import DetailMixin, UpdateMixin

class Index(View):
	def get(self, request):
		return redirect(reverse('qna:questions'))

class QuestionsView(ListView):
	queryset = Question.objects.order_by('-date')
	template_name = 'qna/all_questions.html'
	context_object_name = 'questions'

class QuestionView(DetailMixin):
	model = Question
	template_name = 'qna/detail.html'
	context_object_name = 'question'
	error_url = reverse_lazy('qna:questions')
	
	def function(self):
		self.object.views += 1
		self.object.save()

	success_func = function

class MyQuestionsView(ListView):
	template_name = 'qna/my_questions.html'
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
	template_name = 'qna/update.html'
	success_url = reverse_lazy('qna:questions')

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

class UpdateQuestionView(UpdateMixin):
	model = Question
	form_class = QuestionForm
	template_name = 'qna/update.html'
	success_url = reverse_lazy('qna:questions_my')
	success_msg = 'Ваш вопрос был успешно обновлен'
	new_kwargs = {'update': True}

class QuestionDelete(MessagesMixin, DeleteView):
	model = Question
	success_url = reverse_lazy('qna:questions_my')
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