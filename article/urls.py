from django.urls import path
from article import views
app_name = 'article'
urlpatterns = [
    path('get_article/', views.get_article, name='get_article'),
    path('upload_img/', views.upload_img, name='upload_img'),
    path('get_all_img/', views.get_all_img, name='get_all_img'),
    path('add_article/', views.add_article, name='add_article'),
    path('edit/', views.edit, name='edit'),
    path('operate/', views.operate, name='operate'),
]
