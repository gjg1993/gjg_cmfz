from django.urls import path
from banner import views
app_name = 'banner'
urlpatterns = [
    path('get_banner/', views.get_banner, name='get_banner'),
    path('add_banner/', views.add_banner, name='add_banner'),
    path('operate/', views.operate, name='operate'),
    path('edit/', views.edit, name='edit'),
    path('edit_logic/', views.edit_logic, name='edit_logic'),



]
