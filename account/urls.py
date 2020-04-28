from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
	path('register/', views.UserRegisterView.as_view(), name = 'register'),
	path('login/', views.UserLoginView.as_view(), name = 'login'),
	path('profile/', views.ProfileView.as_view(), name = 'profile'),
	path('profile/settings', views.SettingsView.as_view(), name = 'settings'),
	path('myarticles/', views.MyArticlesView.as_view(), name = 'my_articles'),
	path('myarticles/new/', views.NewArticleView.as_view(), name = 'new_article'),
	path('myarticles/edit/<int:pk>/', views.EditArticleView.as_view(), name = 'edit_article'),
	path('myarticles/delete/<int:pk>/', views.DeleteArticleView.as_view(), name = 'delete_article'),
	path('notifications/', views.NotificationsView.as_view(), name = 'notifications'),
	path('favourite/', views.FavouriteView.as_view(), name = 'favourite'),
]