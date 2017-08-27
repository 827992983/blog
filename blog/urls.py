"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from admin import views as admin_views
from articles import views as articles_views

urlpatterns = [
    url(r'^login', admin_views.login, name='login'),
    url(r'^logout', admin_views.logout, name='logout'),
    url(r'^admin', admin_views.index, name='admin'),
    url(r'^addArticle', admin_views.addArticle, name='addArticle'),
    url(r'^modifyArticle', admin_views.modifyArticle, name='modifyArticle'),
    url(r'^getArticleTitles', admin_views.getArticleTitles, name='getArticleTitles'),
    url(r'^getArticleContent', admin_views.getArticleContent, name='getArticleContent'),
    url(r'^getArticleType', admin_views.getArticleType, name='getArticleType'),
    url(r'^$', articles_views.index, name='home'),
]
