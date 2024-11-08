from django.urls import path
from . import views

urlpatterns = [
    # path('get_messages/', views.get_messages, name='get_messages'),
    # path('send_message/', views.send_message, name='send_message'),
    path('admin/chat/<str:room_name>/send', views.send_message_admin, name='send_message_admin'),
]
