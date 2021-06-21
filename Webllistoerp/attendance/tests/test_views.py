from django.test import TestCase
from chat.models import OnetoOneMessage
from django.utils import timezone
from django.test import Client
from django.urls import reverse



# class AttendanceFormViewTest(TestCase):

# 	def setUp(self):
# 		self.d = Client()
# 		self.attendance_url = reverse('attendance-form')

# 	def test_creategroup_page(self):
# 		response = self.d.get(self.attendance_url)
# 		self.assertEqual(response.status_code, 200)
# 		self.assertTemplateUsed(response, 'attendance/att_form.html')


# class DayoffFormViewTest(TestCase):

# 	def setUp(self):
# 		self.d = Client()
# 		self.attendance_url = reverse('dayoff-form')

# 	def test_creategroup_page(self):
# 		response = self.d.get(self.attendance_url)
# 		self.assertEqual(response.status_code, 200)
# 		self.assertTemplateUsed(response, 'attendance/dayoff_form.html')



# class LeaveInfoViewTest(TestCase):

# 	def setUp(self):
# 		self.d = Client()
# 		self.attendance_url = reverse('leave-info')

# 	def test_creategroup_page(self):
# 		response = self.d.get(self.attendance_url)
# 		self.assertEqual(response.status_code, 200)
# 		self.assertTemplateUsed(response, 'attendance/leaveinfo.html')


# class HolidayInfoViewTest(TestCase):

# 	def setUp(self):
# 		self.d = Client()
# 		self.attendance_url = reverse('holidays-page')

# 	def test_creategroup_page(self):
# 		response = self.d.get(self.attendance_url)
# 		self.assertEqual(response.status_code, 200)
# 		self.assertTemplateUsed(response, 'attendance/holiday.html')





# Failed Test Cases

# class SearchAttendanceViewTest(TestCase):

# 	def setUp(self):
# 		self.d = Client()
# 		self.attendance_url = reverse('attendance-info')

# 	def test_creategroup_page(self):
# 		response = self.d.get(self.attendance_url)
# 		self.assertEqual(response.status_code, 200)
# 		self.assertTemplateUsed(response, 'attendance/attendance_form.html')


# class NotificationViewTest(TestCase):

# 	def setUp(self):
# 		self.d = Client()
# 		self.attendance_url = reverse('notifications_page')

# 	def test_creategroup_page(self):
# 		response = self.d.get(self.attendance_url)
# 		self.assertEqual(response.status_code, 200)
# 		self.assertTemplateUsed(response, 'attendance/notifications.html')


# class TimesheetViewTest(TestCase):

# 	def setUp(self):
# 		self.d = Client()
# 		self.attendance_url = reverse('timesheet-record')

# 	def test_creategroup_page(self):
# 		response = self.d.get(self.attendance_url)
# 		self.assertEqual(response.status_code, 200)
# 		self.assertTemplateUsed(response, 'attendance/timesheet_record.html')







# class YourTestClass(TestCase):
# 	@classmethod
# 	def setUpTestData(cls):
# 		print("setUpTestData: Run once to set up non-modified data for all class methods.")
# 		pass

# 	def setUp(self):
# 		print("This is SetUp")
# 		pass

# 	def test_attendance_form(self):
# 		self.c = Client()
# 		response = self.c.get("/attendance/form")
# 		print("attendance form page")
# 		print(response.status_code)
# 		self.assertEqual(response.status_code, 200)

# 	def test_dayoff_form(self):
# 		self.d = Client()
# 		response = self.d.get("/attendance/dayoff/form")
# 		print("attendance dayoff form page")
# 		print(response.status_code)
# 		self.assertEqual(response.status_code, 200)

# 	def test_leaveinfo_form(self):
# 		self.d = Client()
# 		response = self.d.get("/attendance/leave/info")
# 		print("attendance leaveinfo form page")
# 		print(response.status_code)
# 		self.assertEqual(response.status_code, 200)

# 	def test_holiday_form(self):
# 		self.d = Client()
# 		response = self.d.get("/attendance/holidays")
# 		print("holiday display page")
# 		print(response.status_code)
# 		self.assertEqual(response.status_code, 200)

	# Test methods not executing properly

	# def test_search_attendance(self):
	# 	self.d = Client()
	# 	response = self.d.get("attendance/info")
	# 	print("search attendance form page")
	# 	print(response.status_code)
	# 	self.assertEqual(response.status_code, 200)

	# def test_notification_form(self):
	# 	self.d = Client()
	# 	response = self.d.get("/attendance/notifications_page")
	# 	print("notifications form page")
	# 	print(response.status_code)
	# 	self.assertEqual(response.status_code, 200)

	# def test_timesheet_form(self):
	# 	self.d = Client()
	# 	response = self.d.get("/timesheet/record/")
	# 	print("timesheet form page")
	# 	print(response.status_code)
	# 	self.assertEqual(response.status_code, 200)






