from django.test import TestCase
from chat.models import OnetoOneMessage
from attendance.models import HolidayData, UserDayoffData
from django.utils import timezone
from django.test import Client



class HolidayModelTest(TestCase):

	def setUp(self):
		e = "2021-06-17"
		p = "Testing Day"
		self.user = HolidayData.objects.create(date = e, occasion = p)

	def test_first_name(self):
		self.assertEqual(self.user.occasion, 'Testing Day')



class DayoffFormModelTest(TestCase):

	def setUp(self):
		name = "alban.shhai32"
		calen1 = '2021-06-17'
		calen2 = '2021-06-19'
		self.user = UserDayoffData.objects.create(
                                  				name = name,
                                  				leave_request_date = calen1,
                                  				leave_from = calen1,
                                  				leave_to = calen2,
                                  				hr_approval = "Pending",
                                  				tl_approval = "Pending",
                                  				leave_reason = '\t\t\t\tLeave for Vaccination'
                               					)

	def test_first_name(self):
		self.assertEqual(self.user.name, 'alban.shhai32')

