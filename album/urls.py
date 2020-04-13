"""gjg_cmfz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from album import views
app_name = 'album'
urlpatterns = [
    path('get_album/', views.get_album, name='get_album'),
    path('get_chapter/', views.get_chapter, name='get_chapter'),
    path('operate/', views.operate, name='operate'),
    path('add_chapter/', views.add_chapter, name='add_chapter'),
    path('get_chapter_name/', views.get_chapter_name, name='get_chapter_name'),
    path('del_chapter/', views.del_chapter, name='del_chapter'),
    path('edit_chapter/', views.edit_chapter, name='edit_chapter'),



]
