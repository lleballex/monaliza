"""monaliza URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from monaliza import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView, RedirectView

from it_articles.sitemap import PostsSitemap, PostsIndexSitemap
from account.sitemap import AccountIndexSitemap
from qna.sitemap import QuestionsSitemap
from start_page.sitemap import StartPageIndexSitemap

sitemaps = {
    'posts': PostsSitemap,
    'posts_index': PostsIndexSitemap,
    'account_index': AccountIndexSitemap,
    'questions': QuestionsSitemap,
    'start_page_index': StartPageIndexSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('start_page.urls')),
    path('account/', include('account.urls')),
    path('posts/', include('it_articles.urls')),
    path('qna/', include('qna.urls')),
    path('search/', include('search.urls')),
    path('support/', include('support.urls')),
    path('about/', TemplateView.as_view(template_name = 'about.html'), name = 'about'),
    path('favicon.ico/', RedirectView.as_view(url = '/static/favicon.ico', permanent = True), name = 'favicon'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name = 'robots.txt', content_type='text/plain')),
    path('all_ad', TemplateView.as_view(template_name = 'all_ad.html')),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

handler404 = 'monaliza.utils.handler_404'