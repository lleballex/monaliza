from django.urls import path
from . import views

app_name = 'qna'
urlpatterns = [
	path('', views.redirect_to_questions, name = 'redirect_to_questions'),
	path('questions/all', views.AllQuestionsView.as_view(), name = 'all_questions'),
]