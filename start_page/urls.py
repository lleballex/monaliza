from django.urls import path
from . import views

app_name = 'start_page'
urlpatterns = [
	path('', views.MainView.as_view(), name = 'main_view'),
]