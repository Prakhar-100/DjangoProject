from django.shortcuts import render
from django.http import HttpResponse
# from django.views.decorators.csrf import csrf_exempt
# from twilio.rest import TwilioRestClient as Call
from twilio.rest import Client
# from twilio.twiml.voice_response import VoiceResponse
from core.forms import CallingForm

# Create your views here.
# twiml='<Response><Say>Ahoy there!</Say></Response>'
# @csrf_exempt
# Phone Number SID
# PN45c8ae16547c0c82b1ff6a041945bda2
# MESSAGING_SERVICE_SID = ZS9a111cae1ab7a3573a63226a61ca11a9

def my_call_router():

	From_Number = '+12254143610'
	To_Number = '+916260336626'
	Src_path = "http://demo.twilio.com/docs/voice.xml"
	Account_Sid = "ACf18711ab713d4b15a1ddc654377761d9"
	Auth_Token = "cbe252231673c4b318a1903db38fc4a6"

	client = Client(Account_Sid, Auth_Token)
	print("Call initiated")

	call = client.calls.create(
						url = Src_path,
						to = To_Number, 
						from_ = From_Number, 
						)
	print(call.sid)

	# service = client.proxy.services.create(unique_name='unique_name')
	# print(service.sid)

	# session = client.proxy.services('KSXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX') \
	# 								.sessions \
	# 								.create(unique_name='MyFirstSession')
	# print(session.sid)


	# phone_number = client.proxy.services('ZS9a111cae1ab7a3573a63226a61ca11a9').phone_numbers.create(sid='ACf18711ab713d4b15a1ddc654377761d9')
	# print(phone_number.sid)


	print("Call has been triggered successfully !")
	



def index(request):
	form = CallingForm()

	if request.method ==  'POST':
		form = CallingForm(request.POST)
		if form.is_valid():
			name = form.cleaned_data.get('name')
			mob = form.cleaned_data.get('mob')
			my_call_router()
			return render(request, 'core/index.html', {'form': form})

	return render(request, 'core/index.html', {'form': form})