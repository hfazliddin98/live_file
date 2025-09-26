from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('room/<int:room_id>/', views.room, name='room'),
    path('create/', views.create_room, name='create_room'),
    path('delete-content/<int:message_id>/<str:content_type>/', views.delete_message_content, name='delete_content'),
    path('delete-room/<int:room_id>/', views.delete_room, name='delete_room'),
]
