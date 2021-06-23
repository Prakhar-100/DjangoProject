from django.test import TestCase, RequestFactory
from chat.models import OnetoOneMessage
from django.utils import timezone
from django.test import Client
from django.urls import reverse
from core.models import CustomUser
from core.views import index, Sign_up, Promodel, designation_update
from django.contrib.auth.models import AnonymousUser, User



class IndexPageViewTest(TestCase):

	def setUp(self):
		# Every test needs access to the request factory.
		self.factory = RequestFactory()
		f = "Piyush"
		l = "Singh"
		e = "piyush_singh@gmail.com"
		p = "Tintu2soni"
		self.member = CustomUser.objects.create(first_name=f, last_name=l, email=e,password=p,designation='Director')
		self.attendance_url = reverse('index')

	def test_creategroup_page(self):
		# Create an instance of a GET request.
		request = self.factory.get(self.attendance_url)
	    # Recall that middleware are not supported. You can simulate a
	    # logged-in user by setting request.user manually.
		request.user = self.member
	    # Or you can simulate an anonymous user by setting request.user to
	    # an AnonymousUser instance.
		response = index(request)
		self.assertEqual(response.status_code, 200)


class SignUpPageViewTest(TestCase):

	def setUp(self):
		# Every test needs access to the request factory.
		self.factory = RequestFactory()
		f = "Piyush"
		l = "Singh"
		e = "piyush_singh@gmail.com"
		p = "Tintu2soni"
		self.member = CustomUser.objects.create(first_name=f, last_name=l, email=e,password=p,designation='Director')
		self.attendance_url = reverse('sign_up')

	def test_creategroup_page(self):
		# Create an instance of a GET request.
		request = self.factory.get(self.attendance_url)
	    # Recall that middleware are not supported. You can simulate a
	    # logged-in user by setting request.user manually.
		request.user = self.member
	    # Or you can simulate an anonymous user by setting request.user to
	    # an AnonymousUser instance.
		response = Sign_up.as_view()(request)
		self.assertEqual(response.status_code, 200)


class ProfilePageViewTest(TestCase):

	def setUp(self):
		# Every test needs access to the request factory.
		self.factory = RequestFactory()
		f = "Piyush"
		l = "Singh"
		e = "piyush_singh@gmail.com"
		p = "Tintu2soni"
		self.member = CustomUser.objects.create(first_name=f, last_name=l, email=e,password=p,designation='Director')
		self.attendance_url = reverse('promodel')

	def test_creategroup_page(self):
		# Create an instance of a GET request.
		request = self.factory.get(self.attendance_url)
	    # Recall that middleware are not supported. You can simulate a
	    # logged-in user by setting request.user manually.
		request.user = self.member
	    # Or you can simulate an anonymous user by setting request.user to
	    # an AnonymousUser instance.
		response = Promodel.as_view()(request)
		self.assertEqual(response.status_code, 200)
		

class DesignationUpdateViewTest(TestCase):

	def setUp(self):
		# Every test needs access to the request factory.
		self.factory = RequestFactory()
		f = "Piyush"
		l = "Singh"
		e = "piyush_singh@gmail.com"
		p = "Tintu2soni"
		self.member = CustomUser.objects.create(first_name=f, last_name=l, email=e,password=p,designation='Director')
		self.attendance_url = reverse('designationupdate')

	def test_creategroup_page(self):
		# Create an instance of a GET request.
		request = self.factory.get(self.attendance_url)
	    # Recall that middleware are not supported. You can simulate a
	    # logged-in user by setting request.user manually.
		request.user = self.member
	    # Or you can simulate an anonymous user by setting request.user to
	    # an AnonymousUser instance.
		response = designation_update(request)
		self.assertEqual(response.status_code, 200)



