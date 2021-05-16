from django.urls import path
from . import views

app_name = 'friend_app'

urlpatterns = [
    path('', views.user_list, name='list'),
    path('<int:friendly_user_id>/', views.user_retrieve, name='retrieve'),
    path('<int:user_id_1>/start_friendship/', views.start_friendship, name='start_friendship'),
    path('<int:user_id_1>/end_friendship/', views.end_friendship, name='end_friendship'),
]
