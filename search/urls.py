from django.urls import path
from . import views

app_name = 'search'
urlpatterns = [
	path('', views.SearchView.as_view(), name = 'search'),
	path('users/<str:username>/', views.UserView.as_view(), name = 'user_page')
]