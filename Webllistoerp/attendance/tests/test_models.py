from django.test import TestCase
from chat.models import OnetoOneMessage
from attendance.models import HolidayData, UserDayoffData, TimeSheetData, DatewiseData, AttendanceData
from core.models import CustomUser
from django.utils import timezone
from django.test import Client
import datetime



class HolidayModelTest(TestCase):

	def setUp(self):
		e = "2021-06-17"
		p = "Testing Day"
		self.user = HolidayData.objects.create(date = e, occasion = p)

	def test_first_name(self):
		self.assertEqual(self.user.occasion, 'Testing Day')
		self.assertTrue(isinstance(self.user, HolidayData))



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


class TimeSheetModelTest(TestCase):

	def setUp(self):
		# obj1 = CustomUser.objects.get(id = 5)
		# use = '5'
		n = "Piyush Singh"
		d = datetime.date(2021, 6, 25)
		st = "11:50:21"
		ft = "12:05:40"
		tt = "00:02:00"
		self.user = TimeSheetData.objects.create(name = n,
												 date = d,
												 start_time = st,
												 finish_time = ft,
												 total_time =  tt
												 )

	def test_first_name(self):
		self.assertEqual(self.user.date, datetime.date(2021, 6, 25))
		self.assertTrue(isinstance(self.user, TimeSheetData))


class DatewiseModelTest(TestCase):

	def setUp(self):
		n = "alban_sheikh"
		d = datetime.date(2021, 6, 23)
		wk = "Thursday"
		ti = "08:30 PM"
		to = "07:30 PM"
		ws = "Full Day Working"
		self.user = DatewiseData.objects.create(name = n,
												date = d,
												week = wk,
												time_in = ti,
												time_out =  to,
												work_status = ws
												)

	def test_first_name(self):
		self.assertEqual(self.user.date, datetime.date(2021, 6, 23))
		self.assertTrue(isinstance(self.user, DatewiseData))


class AttendanceDataModelTest(TestCase):

	def setUp(self):
		self.user = AttendanceData.objects.create(timestamp = '19-Apr-2021 (19:15:35.263131)',
												  emp = "meghraj_pardesi")

	def test_first_name(self):
		self.assertEqual(self.user.emp, "meghraj_pardesi")
		self.assertTrue(isinstance(self.user, AttendanceData))





