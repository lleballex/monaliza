from django.urls import path
from . import views

app_name = 'it_articles'
urlpatterns = [
	path('all/', views.AllArticlesView.as_view(), name = 'articles_all'),
	path('detail/<int:pk>/', views.DetailArticleView.as_view(), name = 'detail'),
	path('search/', views.SearchView.as_view(), name = 'search'),
	path('send_comment/<int:pk>', views.SendComment.as_view(), name = 'send_comment'),
	path('detail/<int:pk>/delete_comment/', views.DeleteComment.as_view(), name = 'delete_comment'),
	path('like_article', views.LikeArticle.as_view(), name = 'like_article'),
]