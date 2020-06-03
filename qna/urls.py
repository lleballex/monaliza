from django.urls import path
from . import views, ajax

app_name = 'qna'
urlpatterns = [
	path('', views.Index.as_view(), name = 'index'),
	path('questions/', views.QuestionsView.as_view(), name = 'questions'),
	path('questions/<int:pk>/', views.QuestionView.as_view(), name = 'question'),
	path('questions/<int:pk>/update/', views.UpdateQuestionView.as_view(), name = 'question_update'),
	path('questions/<int:pk>/delete/', views.DeleteQuestion.as_view(), name = 'question_delete'),
	path('questions/my/', views.MyQuestionsView.as_view(), name = 'questions_my'),
	path('questions/new/', views.NewQuestionView.as_view(), name = 'question_new'),
	path('answers/my/', views.MyAnswersView.as_view(), name = 'answers_my'),
	path('answers/<int:pk>/update/', views.UpdateAnswerView.as_view(), name = 'answer_update'),
	path('answers/<int:pk>/delete/', views.DeleteAnswer.as_view(), name = 'answer_delete_notajax'),
	
	path('answer_send/', ajax.AnswerSend.as_view(), name = 'answer_send'),
	path('answer_delete/', ajax.AnswerDelete.as_view(), name = 'answer_delete'),
	path('answer_right/', ajax.AnswerRight.as_view(), name = 'answer_right'),
]