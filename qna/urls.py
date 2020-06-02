from django.urls import path
from . import views, ajax

app_name = 'qna'
urlpatterns = [
	path('', views.Index.as_view(), name = 'index'),
	path('questions/all/', views.QuestionsView.as_view(), name = 'questions'),
	path('questions/', views.QuestionView.as_view(), name = 'question'),
	path('questions/my/', views.MyQuestionsView.as_view(), name = 'questions_my'),
	path('questions/my/new/', views.NewQuestionView.as_view(), name = 'question_new'),
	path('questions/my/update/', views.UpdateQuestionView.as_view(), name = 'question_update'),
	
	path('answer_send/', ajax.AnswerSend.as_view(), name = 'answer_send'),
	path('answer_delete/', ajax.AnswerDelete.as_view(), name = 'answer_delete'),
	path('answer_right/', ajax.AnswerRight.as_view(), name = 'answer_right'),
	
	
	path('question/my/delete/<int:pk>/', views.QuestionDelete.as_view(), name = 'delete_question'),
	path('answers/my/', views.MyAnswersView.as_view(), name = 'my_answers'),
	path('answers/my/update/<int:pk>/', views.UpdateAnswerView.as_view(), name = 'answer_update'),
]