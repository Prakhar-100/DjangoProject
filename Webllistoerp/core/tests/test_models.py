from django.test import TestCase
from chat.models import OnetoOneMessage
from core.models import CustomUser, UserHeirarchy
from django.utils import timezone
from django.test import Client

# models test
class SignUpModelTest(TestCase):

	def setUp(self):
		f = "Prakhar1"
		l = "Tharoor"
		e = "shashi_tharoor@gmail.com"
		p = "Tintu2soni"
		self.user = CustomUser.objects.create(first_name=f, last_name=l, email=e,password=p,designation='Web Developer')

	def test_first_name(self):
		self.assertEqual(self.user.first_name, 'Prakhar1')
		self.assertTrue(isinstance(self.user, CustomUser))


class LoginPageTest(TestCase):
	
	def setUp(self):
		pass
		
	def test_login_page(self):
		self.c = Client()
		response = self.c.post('/',{'user_email': 'piyush_singh@gmail.com', 'password':'Tintu2soni'})
		self.assertEqual(response.status_code, 200)


class ProfileModelTest(TestCase):

	def setUp(self):
		# parent = '46'
		# child = ['56', '88']
		# child = CustomUser.objects.get(id = '88')
		self.user = UserHeirarchy.objects.create()

	def test_parent_name(self):
		self.assertEqual(self.user.usernm_id,  None)
		self.assertTrue(isinstance(self.user, UserHeirarchy))
