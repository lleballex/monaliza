from django.urls import path
from . import views, ajax

app_name = 'posts'
urlpatterns = [
	path('', views.Index.as_view(), name = 'index'),
	path('all/', views.PostsView.as_view(), name = 'all'),
	path('<int:pk>/', views.PostView.as_view(), name = 'detail'),
	path('<int:pk>/set_available/', views.PostAvailable.as_view(), name = 'set_available'),	
	path('my/', views.MyPostsView.as_view(), name = 'my'),
	path('my/favourite/', views.FavouritePostsView.as_view(), name = 'favourite'),
	path('my/new/', views.NewPostView.as_view(), name = 'new'),
	path('my/update/<int:pk>/', views.UpdatePostView.as_view(), name = 'update'),
	path('my/delete/<int:pk>/', views.DeletePost.as_view(), name = 'delete'),

	path('post_like/', ajax.PostLike.as_view(), name = 'post_like'),
	path('comment_send/', ajax.CommentSend.as_view(), name = 'comment_send'),
	path('comment_delete/', ajax.CommentDelete.as_view(), name = 'comment_delete'),
]