from django.urls import path
from api import views
app_name = 'api'
urlpatterns = [
    path('first_page/', views.first_page, name='first_page'),
    path('get_album_chapter/', views.get_album_chapter, name='get_album_chapter'),
    path('register/', views.register, name='register'),
    path('edit_user/', views.edit_user, name='edit_user'),
]
