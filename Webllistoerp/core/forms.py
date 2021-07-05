from django import forms
# from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, UserHeirarchy
from multiselectfield import MultiSelectField
from django.core.exceptions import ValidationError



class UserForm(UserCreationForm):
	CHOICES = [
	
		('Web Developer', 'Web Developer'),
		('Project Manager', 'Project Manager'),
		('Tech Leader', 'Tech Leader'),
		('Cheif Technical Officer', 'Cheif Technical Officer'),
		('Director', 'Director')
	
		]
	designation = forms.CharField(widget = forms.Select(choices = CHOICES))

	class Meta:
		model = CustomUser
		fields = ['first_name', 'last_name', 'email', 
		 'password1', 'password2','designation']
		 


class Login_form(forms.Form):
	user_email = forms.EmailField(max_length = 50,widget =forms.EmailInput(
		attrs = {
		'class' : 'form-control',
		'placeholder' : 'Enter User Email'
		}))
	password  = forms.CharField(max_length = 15,widget = forms.PasswordInput(
		attrs = {
		'class' : 'form-control',
		'placeholder' : 'Password'
		}))

	


      


	