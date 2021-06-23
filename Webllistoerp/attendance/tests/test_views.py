from django.test import TestCase, RequestFactory
from chat.models import OnetoOneMessage
from django.utils import timezone
from django.test import Client
from django.urls import reverse
from attendance.views import attendance_form, notifications_page, timesheet_record, delete_not, tl_leave
from core.models import CustomUser
from django.contrib.auth.models import AnonymousUser, User



class AttendanceFormViewTest(TestCase):

	def setUp(self):
		self.d = Client()
		self.attendance_url = reverse('attendance-form')

	def test_creategroup_page(self):
		response = self.d.get(self.attendance_url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'attendance/att_form.html')


class DayoffFormViewTest(TestCase):

	def setUp(self):
		self.d = Client()
		self.attendance_url = reverse('dayoff-form')

	def test_creategroup_page(self):
		response = self.d.get(self.attendance_url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'attendance/dayoff_form.html')


class LeaveInfoViewTest(TestCase):

	def setUp(self):
		self.d = Client()
		self.attendance_url = reverse('leave-info')

	def test_creategroup_page(self):
		response = self.d.get(self.attendance_url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'attendance/leaveinfo.html')


class HolidayInfoViewTest(TestCase):

	def setUp(self):
		self.d = Client()
		self.attendance_url = reverse('holidays-page')

	def test_creategroup_page(self):
		response = self.d.get(self.attendance_url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'attendance/holiday.html')


class SearchAttendanceViewTest(TestCase):

	def setUp(self):
		self.factory = RequestFactory()
		f = "Piyush"
		l = "Singh"
		e = "piyush_singh@gmail.com"
		p = "Tintu2soni"
		self.member = CustomUser.objects.create(first_name=f, last_name=l, email=e,password=p,designation='Director')
		self.attendance_url = reverse('attendance-info')

	def test_creategroup_page(self):
		request = self.factory.get(self.attendance_url)
		request.user = self.member
		response = attendance_form(request)
		self.assertEqual(response.status_code, 200)


class NotificationViewTest(TestCase):

	def setUp(self):
		self.factory = RequestFactory()
		f = "Piyush"
		l = "Singh"
		e = "piyush_singh@gmail.com"
		p = "Tintu2soni"
		self.member = CustomUser.objects.create(first_name=f, last_name=l, email=e,password=p,designation='Director')
		self.attendance_url = reverse('notifications_page')


	def test_creategroup_page(self):
		request = self.factory.get(self.attendance_url)
		request.user = self.member
		response = notifications_page(request)
		self.assertEqual(response.status_code, 200)


class TimesheetViewTest(TestCase):

	def setUp(self):
		# Every test needs access to the request factory.
		self.factory = RequestFactory()
		f = "Piyush"
		l = "Singh"
		e = "piyush_singh@gmail.com"
		p = "Tintu2soni"
		self.member = CustomUser.objects.create(first_name=f, last_name=l, email=e,password=p,designation='Director')
		self.attendance_url = reverse('timesheet-record')

	def test_creategroup_page(self):
		request = self.factory.get(self.attendance_url)
		request.user = self.member
		response = timesheet_record(request)
		self.assertEqual(response.status_code, 200)


# class MakeReadViewTest(TestCase):

# 	def setUp(self):
# 		# Every test needs access to the request factory.
# 		self.factory = RequestFactory()
# 		f = "Piyush"
# 		l = "Singh"
# 		e = "piyush_singh@gmail.com"
# 		p = "Tintu2soni"
# 		self.member = CustomUser.objects.create(first_name=f, last_name=l, email=e,password=p,designation='Director')
# 		# self.attendance_url = reverse('make-read')

# 	def test_creategroup_page(self):
# 		# Create an instance of a GET request.
# 		request = self.factory.get('att/tl/not/45/5/')
# 	    # Recall that middleware are not supported. You can simulate a
# 	    # logged-in user by setting request.user manually.
# 		request.user = self.member
# 	    # Or you can simulate an anonymous user by setting request.user to
# 	    # an AnonymousUser instance.
# 		response = tl_leave(request, 45, 5)
# 		self.assertEqual(response.status_code, 200)






