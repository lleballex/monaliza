from django.urls import path
from . import views

app_name = 'qna'
urlpatterns = [
	path('', views.Redirect.as_view(), name = 'qna'),
	path('questions/all/', views.AllQuestionsView.as_view(), name = 'all_questions'),
	path('questions/detail/<int:pk>/', views.DetailQuestionView.as_view(), name = 'detail'),
	path('questions/detail/<int:pk>/set_answer/', views.SetAnswer.as_view(), name = 'set_answer'),
	path('questions/detail/<int:pk>/delete_answer/', views.DeleteAnswer.as_view(), name = 'delete_answer'),
	path('questions/detail/<int:pk>/set_right_answer/', views.SetRightAnswer.as_view(), name = 'set_right_answer'),
	path('questions/detail/<int:pk>/delete_right_answer/', views.DeleteRightAnswer.as_view(), name = 'delete_right_answer'),
	path('myquestions/', views.MyQuestionsView.as_view(), name = 'my_questions'),
	path('myquestions/new/', views.NewQuestionView.as_view(), name = 'new_question'),
]