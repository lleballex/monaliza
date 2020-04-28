from django.contrib import admin
from account.models import User, Notification, FavouriteArticle

admin.site.register(User)
admin.site.register(Notification)
admin.site.register(FavouriteArticle)