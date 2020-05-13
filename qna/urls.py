from django.urls import path
from . import views

app_name = 'qna'
urlpatterns = [
	path('', views.redirect_to_questions, name = 'redirect_to_questions'),
	path('questions/all/', views.AllQuestionsView.as_view(), name = 'all_questions'),
	path('questions/detail/<int:pk>/', views.DetailQuestionView.as_view(), name = 'detail'),
	path('questions/detail/<int:pk>/set_answer/', views.SetAnswer.as_view(), name = 'set_answer'),
	path('questions/detail/<int:pk>/delete_answer/', views.DeleteAnswer.as_view(), name = 'delete_answer'),
	path('questions/detail/<int:pk>/set_right_answer/', views.SetRightAnswer.as_view(), name = 'set_right_answer'),
	path('questions/detail/<int:pk>/delete_right_answer/', views.DeleteRightAnswer.as_view(), name = 'delete_right_answer'),
]