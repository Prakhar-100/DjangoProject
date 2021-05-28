from django.shortcuts import render, redirect
from .models import TextMessage
import datetime

# def index(request):
# 	print("here")
# return render(request, 'chat/index.html')

def index(request):
    return render(request,'chat/index.html') 

def room(request, room_name):
	name = request.user.first_name +"  "+ request.user.last_name

	if request.method == 'POST':
		txt = request.POST['mytext']
		TextMessage.objects.create(e_id = request.user.id,
			                       e_name = name,
			                       e_message = txt,
			                       e_time =  datetime.datetime.today().time()
			                       )

	text_msg = TextMessage.objects.all()
	return render(request, 'chat/room.html',{'room_name': room_name})