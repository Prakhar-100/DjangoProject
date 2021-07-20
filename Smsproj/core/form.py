from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser






class MessageForm(forms.Form):
	full_name = forms.CharField(max_length = 50)
	mobile_no = forms.CharField(max_length = 12)
	# password = forms.CharField(max_length = 20, widget = forms.PasswordInput())


class OtpForm(forms.Form):
	pin = forms.CharField(max_length = 6)

class SmsForm(forms.Form):
	textmsg = forms.CharField(max_length = 100)


	


