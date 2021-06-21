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




# class YourTestClass(TestCase):
# 	@classmethod
# 	def setUpTestData(cls):
# 		print("setUpTestData: Run once to set up non-modified data for all class methods.")
# 		pass

# 	def setUp(self):
# 		print("This is SetUp")
# 		pass

# 	def test_chat_create_group(self):
# 		self.d = Client()
# 		response = self.d.get("/chat/create/group/")
# 		print("create channel form page")
# 		print(response.status_code)
# 		self.assertEqual(response.status_code, 200)

# 	def test_chat_create_onegroup(self):
# 		self.d = Client()
# 		response = self.d.get("/chat/create/channel/")
# 		print("create one channel form page")
# 		print(response.status_code)
# 		self.assertEqual(response.status_code, 200)

# 	def test_chat_one_roomgroup(self):
# 		self.d = Client()
# 		response = self.d.get("/chat/one/43")
# 		print("one room channel page")
# 		print(response.status_code)
# 		self.assertEqual(response.status_code, 301)

# 	def test_chat_roomgroup(self):
# 		self.d = Client()
# 		response = self.d.get("/chat/group/36")
# 		print("group room channel page")
# 		print(response.status_code)
# 		self.assertEqual(response.status_code, 301)



