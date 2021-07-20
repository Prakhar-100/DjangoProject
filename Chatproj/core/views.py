from django.shortcuts import render, redirect
from django.http import HttpResponse
from twilio.rest import Client
from .models import Room
from django.conf import settings
from django.http import JsonResponse

from faker import Faker
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import ChatGrant

import os

fake = Faker()


# Create your views here.
# SERVICE_SID = 'IS7d9077573c6949a2978df01fb064f166'
# TWILIO_API_KEY = 'SK082f7f9e8be221b7a16befa796e73115'
# TWILIO_API_SECRET = 'Pidxm1BVr1iWSNEOTYDf5rWEdXup8hUh'




# core/views.py


def all_rooms(request):
	rooms = Room.objects.all()
	return render(request, 'core/index.html', {'rooms': rooms})

def room_detail(request, slug):
	room = Room.objects.get(slug=slug)
	return render(request, 'core/room_detail.html', {'room': room})


def token(request):
    identity = request.GET.get('identity', fake.user_name())
    device_id = request.GET.get('device', 'default')  # unique device ID

    account_sid = settings.TWILIO_ACCOUNT_SID
    api_key = settings.TWILIO_API_KEY
    api_secret = settings.TWILIO_API_SECRET
    chat_service_sid = settings.TWILIO_CHAT_SERVICE_SID

    token = AccessToken(account_sid, api_key, api_secret, identity=identity)

    # Create a unique endpoint ID for the device
    endpoint = "MyDjangoChatRoom:{0}:{1}".format(identity, device_id)

    if chat_service_sid:
        chat_grant = ChatGrant(endpoint_id=endpoint,
                               service_sid=chat_service_sid)
        token.add_grant(chat_grant)

    response = {
        'identity': identity,
        'token': token.to_jwt().decode('utf-8')
    }

    return JsonResponse(response)

# def index(request):
# 	return render(request, 'core/index.html', {})

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
# account_sid = 'ACf18711ab713d4b15a1ddc654377761d9'
# auth_token = 'cbe252231673c4b318a1903db38fc4a6'
# client = Client(account_sid, auth_token)

# conversation = client.conversations.create(friendly_name='My First Conversation')

# print(conversation.sid)

# binding = client.chat.services('ISXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX') \
#                      .bindings('BSXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX') \
#                      .fetch()

# print(binding.sid)

# participant = client.conversations \
#     .conversations('CHXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX') \
#     .participants \
#     .create(
#          messaging_binding_address='<Your Personal Mobile Number>',
#          messaging_binding_proxy_address='<Your purchased Twilio Phone Number>'
#      )

# print(participant.sid)


# {"sid": "ISe06deb77506544b8a8696cd4801a874e", "account_sid": "ACf18711ab713d4b15a1ddc654377761d9",
#  "friendly_name": "Chat Testing",
#  "date_created": "2021-07-08T09:45:54Z", "date_updated": "2021-07-08T09:45:54Z",
#  "default_service_role_sid": "RLa84909a169c840f6b9436f5428934c87",
#  "default_channel_role_sid": "RL6dbcbc2f6159477ba11a41a9aa2dca5c",
#  "default_channel_creator_role_sid": "RL9ec556955d8044138f3d78185a330b5f",
#  "read_status_enabled": true, "reachability_enabled": false,
#  "typing_indicator_timeout": 5, "consumption_report_interval": 10,
#  "webhooks": null, "pre_webhook_url": null, "post_webhook_url": null,
#  "webhook_method": null, "webhook_filters": null,
#  "notifications": {"removed_from_channel": {"enabled": false},
#  "log_enabled": false, "added_to_channel": {"enabled": false},
#  "new_message": {"enabled": false}, "invited_to_channel": {"enabled": false}},
#  "limits": {"user_channels": 250, "channel_members": 100, "actions_per_second": 30},
#  "url": "https://ip-messaging.twilio.com/v1/Services/ISe06deb77506544b8a8696cd4801a874e",
#  "links": {"channels": "https://ip-messaging.twilio.com/v1/Services/ISe06deb77506544b8a8696cd4801a874e/Channels",
#  "roles": "https://ip-messaging.twilio.com/v1/Services/ISe06deb77506544b8a8696cd4801a874e/Roles",
#  "users": "https://ip-messaging.twilio.com/v1/Services/ISe06deb77506544b8a8696cd4801a874e/Users"}}


