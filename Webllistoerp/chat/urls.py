# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('create/channel/', views.CreateChannel.as_view(), name = 'create-group'),
    path('group/<int:id>/', views.GroupChat.as_view(), name = 'group-chat-room'),
    path('one/<int:id>/', views.OneChatRoom.as_view(), name = 'one-chat-room'),
    path('create/group/', views.CreateOneChannel.as_view(), name = 'create-one-group'),

    # AJAX Call
    path('ajax/load-names/', views.load_channel_usernames, name = 'ajax_load_channel_names'),
    # path('ajax/load-data/', views.load_channel_data, name = 'ajax_load_channel_data'),

]
