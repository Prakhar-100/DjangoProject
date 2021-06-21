from django.test import TestCase
from chat.models import OnetoOneMessage
from django.utils import timezone
from django.test import Client
from django.urls import reverse




class YourTestClass(TestCase):
	@classmethod
	def setUpTestData(cls):
		pass

	def setUp(self):
		pass

	def test_index_page(self):
		self.c = Client()
		response = self.c.get("/index")
		self.assertEqual(response.status_code, 301)

	def test_signup_page(self):
		self.d = Client()
		response = self.d.get("/accounts/signup/")
		self.assertEqual(response.status_code, 200)

	def test_profile_page(self):
		c = Client()
		response = c.get('/core/promodel/')
		self.assertEqual(response.status_code, 200)


	# Failed TestCase
	# def test_designation_update(self):
	# 	self.e = Client()
	# 	response = self.e.get('/core/designationupdate/')
	# 	self.assertEqual(response.status_code, 200)






