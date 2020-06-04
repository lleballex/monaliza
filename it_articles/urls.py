from django.urls import path
from . import views, ajax

app_name = 'posts'
urlpatterns = [
	path('', views.PostsView.as_view(), name = 'posts'),
	path('<int:pk>/', views.PostView.as_view(), name = 'post'),
	path('<int:pk>/set_available/', views.AvailablePost.as_view(), name = 'set_available'),	
	path('my/', views.MyPostsView.as_view(), name = 'my'),
	path('favourite/', views.FavouritePostsView.as_view(), name = 'favourite'),
	path('new/', views.NewPostView.as_view(), name = 'new'),
	path('<int:pk>/update/', views.UpdatePostView.as_view(), name = 'update'),
	path('<int:pk>/delete/', views.DeletePost.as_view(), name = 'delete'),

	path('post_like/', ajax.PostLike.as_view(), name = 'post_like'),
	path('comment_send/', ajax.CommentSend.as_view(), name = 'comment_send'),
	path('comment_delete/', ajax.CommentDelete.as_view(), name = 'comment_delete'),
]