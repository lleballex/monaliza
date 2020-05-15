from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
	path('', views.Redirect.as_view(), name = 'account'),
	path('register/', views.UserRegisterView.as_view(), name = 'register'),
	path('login/', views.UserLoginView.as_view(), name = 'login'),
	path('profile/', views.ProfileView.as_view(), name = 'profile'),
	path('profile/settings', views.SettingsView.as_view(), name = 'settings'),	
	path('notifications/', views.NotificationsView.as_view(), name = 'notifications'),
	path('notifications/set_notifications_not_new/', views.SetNotificationsNotNew.as_view(), name = 'set_notifications_not_new'),
	path('notifications/delete_notification/', views.DeleteNotification.as_view(), name = 'delete_notification'),
	path('favourite/', views.FavouriteView.as_view(), name = 'favourite'),
]