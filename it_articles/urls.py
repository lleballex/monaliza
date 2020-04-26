from django.urls import path
from . import views

app_name = 'it_articles'
urlpatterns = [
	path('all/', views.AllArticlesView.as_view(), name = 'articles_all'),
	path('detail/<int:pk>/', views.DetailArticleView.as_view(), name = 'detail'),
	path('search/', views.SearchView.as_view(), name = 'search'),
	path('detail/<int:pk>/check/', views.Check.as_view(), name = 'check'),
	path('detail/<int:pk>/delete_comment/', views.DeleteComment.as_view(), name = 'delete_comment'),
]