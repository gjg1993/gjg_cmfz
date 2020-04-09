from django.urls import path
from user import views
app_name = 'user'
urlpatterns = [
    path('get_user/', views.get_user, name='get_user'),
    path('add_user/', views.add_user, name='add_user'),
    path('edit/', views.edit, name='edit'),
    path('edit_logic/', views.edit_logic, name='edit_logic'),
    path('operate/', views.operate, name='operate'),
    path('get_data/', views.get_data, name='get_data'),
]
