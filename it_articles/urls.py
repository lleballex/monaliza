from django.urls import path
from . import views

app_name = 'it_articles'
urlpatterns = [
	path('all/', views.AllArticlesView.as_view(), name = 'articles_all'),
	path('detail/<int:pk>/', views.DetailArticleView.as_view(), name = 'detail'),
	path('search/', views.SearchView.as_view(), name = 'search'),
]