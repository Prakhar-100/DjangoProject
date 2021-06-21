from django import forms
# from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, UserHeirarchy
from multiselectfield import MultiSelectField



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


class ProfileForm(forms.ModelForm):
	child = forms.MultipleChoiceField()
	# child = forms.CharField(
	# 	widget = MultiSelectField(is_hidden = True),
	# )

	class Meta:
		model  = UserHeirarchy
		fields = ['usernm', 'child']
		labels = {'child': "Child", 'usernm':'Parent'}

	# def __init__(self, *args, **kwargs):
	# 	super().__init__(*args, **kwargs)
	# 	# self.fields['child'].queryset = CustomUser.objects.all()
	
class DesignationUpdateForm(forms.Form):
	parent = forms.ModelChoiceField(queryset = CustomUser.objects.all())
	child = forms.CharField(widget = forms.TextInput())
	current_designation = forms.CharField(widget = forms.TextInput())
	change_designation = forms.CharField(widget = forms.TextInput())


      


	