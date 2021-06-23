from django.test import TestCase
from chat.models import OnetoOneMessage
from django.utils import timezone
from django.test import Client
from django.urls import reverse



class ChatCreateGroupViewTest(TestCase):

	def setUp(self):
		self.d = Client()
		self.creategroup_url = reverse('create-group')

	def test_creategroup_page(self):
		response = self.d.get(self.creategroup_url)
		self.assertEqual(response.status_code, 200)

class ChatCreateGroupOneViewTest(TestCase):

	def setUp(self):
		self.d = Client()
		self.creategroup_url = reverse('create-one-group')

	def test_creategroup_page(self):
		response = self.d.get(self.creategroup_url)
		self.assertEqual(response.status_code, 200)

class ChatGroupRoomViewTest(TestCase):

	def setUp(self):
		self.d = Client()
		self.creategroup_url = '/chat/group/36'

	def test_creategroup_page(self):
		response = self.d.get(self.creategroup_url)
		self.assertEqual(response.status_code, 301)


class ChatGroupOneRoomViewTest(TestCase):

	def setUp(self):
		self.d = Client()
		self.creategroup_url = '/chat/one/43'

	def test_creategroup_page(self):
		response = self.d.get(self.creategroup_url)
		self.assertEqual(response.status_code, 301)






