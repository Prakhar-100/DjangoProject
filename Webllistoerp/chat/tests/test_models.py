from django.test import TestCase
from chat.models import OnetoOneMessage
from django.utils import timezone
from django.test import Client
from chat.models import ChatGroupList, OnetoOneMessage, GroupMessage
from core.models import CustomUser


class ChatGroupModelTest(TestCase):

	def setUp(self):
		n = "alban.shhai32@gmail.com"
		team = "Corona Warrior Team"
		des = 'This is our Corona Warrior team'
		l3 = ['49', '83', '47', '84']
		ides = CustomUser.objects.filter(id__in = l3)
		self.obj2 = ChatGroupList.objects.create(
												admin_name = n,
												group_name = team,
												description = des, 
		                        				)
		self.obj2.member_name.set(ides)

	def test_admin_name(self):
		self.assertEqual(self.obj2.admin_name, "alban.shhai32@gmail.com")


class ChatOneGroupModelTest(TestCase):

	def setUp(self):
		n = "shakshi.jshai@gmail.com"
		des = 'This is our Corona Warrior team'
		l3 = ['49', '83']
		ides = CustomUser.objects.filter(id__in = l3)
		# obj1 = CustomUser.objects.get(id = l3[0])
		# obj2 = CustomUser.objects.get(id = l3[1])
		self.obj3 = ChatGroupList.objects.create(
                                admin_name = n,
                                group_name =  "Corona Warrior Team",
                                description = des
                                )
		self.obj3.member_name.set(ides)

	def test_admin_name(self):
		self.assertEqual(self.obj3.admin_name, "shakshi.jshai@gmail.com")


class ChatOneRoomModelTest(TestCase):

	def setUp(self):
		txt = 'Testing Message'
		self.user = OnetoOneMessage.objects.create(e_id = '84',
                                       			   e_name = "Alban  Sheikh",
                                       			   e_message = txt,
                                       			   e_time =  "09:16:01.529281",
                                       			   e_groupid = "37"
                                    			  )

	def test_admin_name(self):
		self.assertEqual(self.user.e_name, "Alban  Sheikh")


class ChatGroupRoomModelTest(TestCase):

	def setUp(self):
		txt = 'Testing Message'
		self.user = GroupMessage.objects.create(e_id = '84',
                                    			e_name = "Alban  Sheikh",
                                    			e_message = txt,
                                    			e_time =  "09:16:01.529281",
                                    			e_groupid = "36"
                                   				)

	def test_admin_name(self):
		self.assertEqual(self.user.e_name, "Alban  Sheikh")



	
