from django.urls import path
from . import views

app_name = 'posts'
urlpatterns = [
	path('', views.Redirect.as_view(), name = 'posts'),
	path('all/', views.AllArticlesView.as_view(), name = 'all_posts'),
	path('detail/<int:pk>/', views.DetailArticleView.as_view(), name = 'detail'),
	path('detail/<int:pk>/set_available', views.SetPostAvailable.as_view(), name = 'set_post_available'),
	#path('search/', views.SearchView.as_view(), name = 'search'),
	path('send_comment/<int:pk>', views.SendComment.as_view(), name = 'send_comment'),
	path('detail/<int:pk>/delete_comment/', views.DeleteComment.as_view(), name = 'delete_comment'),
	path('like_article', views.LikeArticle.as_view(), name = 'like_article'),
	path('favourite/', views.FavouritePostsView.as_view(), name = 'favourite'),
	path('myposts/', views.MyArticlesView.as_view(), name = 'my_posts'),
	path('myposts/new/', views.NewArticleView.as_view(), name = 'new_post'),
	path('myposts/edit/<int:pk>/', views.EditArticleView.as_view(), name = 'edit_post'),
	path('myposts/delete/<int:pk>/', views.DeleteArticleView.as_view(), name = 'delete_post'),
]