# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='chat'),
    path('<str:room_name>/', views.room, name='room'),
    path('create/channel/', views.create_channel, name = 'create-group'),
    path('group/<int:id>/', views.GroupChat.as_view(), name = 'group-chat-room'),
    path('one/<int:id>/', views.OneChatRoom.as_view(), name = 'one-chat-room'),
    path('user/room/', views.user_chat_room, name = 'user-chat-room'),
    path('create/group/', views.createone_channel, name = 'create-one-group'),

    # AJAX Call
    path('ajax/load-names/', views.load_channel_usernames, name = 'ajax_load_channel_names'),
    # path('ajax/load-data/', views.load_channel_data, name = 'ajax_load_channel_data'),

]
