from django.test import TestCase
from chat.models import OnetoOneMessage
from core.models import CustomUser, UserHeirarchy
from django.utils import timezone
from django.test import Client
from core.forms import UserForm, Login_form
from core.models import CustomUser
from django.contrib.auth import authenticate

# models test
class SignUpFormTest(TestCase):

	def setUp(self):
		pass

	def test_valid_form(self):
		f = "Prakhar1"
		l = "Tharoor"
		e = "shashi_tharoor@gmail.com"
		p = "Tintu2soni"
		self.user = CustomUser.objects.create(first_name = f,
											  last_name = l, 
											  email = e,
											  password = p,
											  designation='Web Developer'
											  )
		self.data = {'first_name': self.user.first_name, 'last_name': self.user.last_name, 'email': self.user.email, 
		              'password1': self.user.password, 'password2': self.user.password,
		               'designation': self.user.designation}
		form = UserForm(data = self.data)
		self.assertTrue(form.is_valid())

	def test_invalid_form(self):
		f = "Prakhar1"
		l = "Tharoor"
		e = "shashi_tharoor@gmail.com"
		p = "Tintu2soni"
		self.user = CustomUser.objects.create(first_name = f,
											  last_name = l, 
											  email = e,
											  password = p,
											  designation=''
											  )
		self.data = {'first_name': self.user.first_name, 'last_name': self.user.last_name, 'email': self.user.email, 
		              'password1': self.user.password, 'password2': self.user.password,
		               'designation': self.user.designation}
		form = UserForm(data = self.data)
		self.assertFalse(form.is_valid())














