# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='chat'),
    path('<str:room_name>/', views.room, name='room'),
    path('create/channel/', views.create_channel, name = 'create-channel'),
    path('group/room/<int:id>/', views.group_chat_room, name = 'group-chat-room'),
    path('user/room/', views.user_chat_room, name = 'user-chat-room'),

    # AJAX Call
    path('ajax/load-names/', views.load_channel_usernames, name = 'ajax_load_channel_names'),
    # path('ajax/load-data/', views.load_channel_data, name = 'ajax_load_channel_data'),

]
