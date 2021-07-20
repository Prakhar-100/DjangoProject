from django.shortcuts import render, redirect
from django.http import HttpResponse
from core.form import MessageForm, OtpForm
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse
from django.conf import settings
from core.form import SmsForm
import random
import os
from twilio.rest import Client
from core.models import TOTP, SmsData

# +12254143610
# twilio recovery code
# HpseuAZ68tJ40dwdNl4-5F6P_hefvdhAu_enHsE7
# PHONE_NUMBER_SID = PN45c8ae16547c0c82b1ff6a041945bda2
# MESSAGING_SERVICE_SID = MG4b173f9c929870838010c35acaac1f07
# MESSAGE COMES IN - https://demo.twilio.com/welcome/sms/reply/

def send_sms(mob, textsms):
	account_sid = 'ACf18711ab713d4b15a1ddc654377761d9'
	auth_token = 'cbe252231673c4b318a1903db38fc4a6'
	client = Client(account_sid, auth_token)


	message = client.messages.create(
	     body = textsms,
	     from_= '+12254143610',
	     to = '+91'+str(mob),
	     )
	# print(client.http_client.last_response.status_code)

def generate_otp():
	list_otp = []

	for i in range(0,6):
		value = random.randint(0,9)
		list_otp.append(str(value))

	str_otp = ''.join(list_otp)
	TOTP.objects.create(token = str_otp)

	return str_otp


def index(request):
	form = MessageForm()
	if request.method == 'POST':
		form = MessageForm(request.POST)
		if form.is_valid():
			name = form.cleaned_data.get('full_name')
			mob = form.cleaned_data.get('mobile_no')
			otp = generate_otp()
			textsms = "Your Twilio verification code is "+str(otp)
			send_sms(mob, textsms)
			return redirect('verify-form')
	return render(request, 'core/form.html', {'form': form})

def verify_index(request):
	form = OtpForm()
	if request.method == 'POST':
		form = OtpForm(request.POST)
		if form.is_valid():
			token = TOTP.objects.last()
			if token.token == form.cleaned_data.get('pin'):
				return redirect('otp-success')
			else:
				return render(request, 'core/verify_form.html', {'form': form, 'msg': 'OTP verification password is incorrect'})
	return render(request, 'core/verify_form.html', {'form': form})

def otp_success(request):
	form = SmsForm()
	sucmsg = "OTP Verification is successfully !!"
	data = SmsData.objects.all()

	if request.method == 'POST':
		form = SmsForm(request.POST)
		if form.is_valid():
			msg = form.cleaned_data.get('textmsg')
			SmsData.objects.create(txt = msg)
			mob = "6260336626"
			send_sms(mob, msg)
			return render(request, 'core/otp_success.html', {'form': form, 'data': data})
	return render(request, 'core/otp_success.html', {'form': form, 'sucmsg': sucmsg})

@csrf_exempt
def sms_response(request):
    # Start our TwiML response
    resp = MessagingResponse()

    # Add a text message
    msg = resp.message("Check out this sweet owl!")

    # Add a picture message
    msg.media("https://demo.twilio.com//Messages")

    return HttpResponse(str(resp))

def sms(request):
	twiml = '<Response><Message>Hello from your Django app!</Message></Response>'
	return HttpResponse(twiml, content_type='text/xml')


	























# def index(request):
# 	form = MessageForm()

# 	# if form.is_valid():
# 		# form = MessageForm(request.POST)
	

# 	return render(request, 'core/form.html', {'form': form})

# and set the environment variables. See http://twil.io/secure
# account_sid = os.environ['TWILIO_ACCOUNT_SID']
# auth_token = os.environ['TWILIO_AUTH_TOKEN']
# client = Client(account_sid, auth_token)

# verification = client.verify \
#                      .services('VAXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX') \
#                      .verifications \
#                      .create(to='+15017122661', channel='sms')

# print(verification.sid)

# twilio api:verify:v2:services:verifications:create \
#     --service-sid VAXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX \
#     --to +15017122661 \
#     --channel call

