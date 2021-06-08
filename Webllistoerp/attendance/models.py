from django.conf import settings
from django.db import models
from core.models import CustomUser 
# from django.utils import timezone
# Create your models here.


class AttendanceModel(models.Model):
	emp = models.OneToOneField(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name='image_of')
	image = models.ImageField(upload_to = "images")
	encod_image = models.CharField(max_length = 2500)

	def __str__(self):
		return str(self.emp) 

class AttendanceData(models.Model):
	# timestamp = models.DateTimeField(default=timezone.now)
	timestamp = models.CharField(max_length = 200)
	emp_id = models.ForeignKey(AttendanceModel,
	    on_delete = models.CASCADE, 
		related_name='user_name', 
		null = True)
	emp = models.CharField(max_length = 100)

	def __str__(self):
		return str(self.emp_id)+" "+str(self.emp)+" "+str(self.timestamp)

class DatewiseData(models.Model):
	name = models.CharField(max_length = 100)
	date = models.DateField()
	week = models.CharField(max_length = 50)
	time_in = models.CharField(max_length = 50)
	time_out = models.CharField(max_length = 50)
	work_status = models.CharField(max_length = 200)

	def __str__(self):
		return str(self.name)+" "+str(self.date)+" "+str(self.time_in)+" "+str(self.time_out)+" "+str(self.work_status)

class HolidayData(models.Model):
	date = models.DateField()
	occasion = models.CharField(max_length = 200)

	def __str__(self):
		return str(self.date)+"  "+str(self.day_name)

class UserDayoffData(models.Model):
	name = models.CharField(max_length = 100)
	leave_request_date = models.DateField(blank=True, null=True)
	leave_from = models.DateField(default = 2)
	leave_to = models.DateField(default = 3)
	hr_approval = models.CharField(max_length = 100)
	tl_approval = models.CharField(max_length = 100)
	leave_reason = models.TextField(max_length = 1500)

class TimeSheetData(models.Model):
	user_id = models.ForeignKey(
		settings.AUTH_USER_MODEL,
	    on_delete = models.CASCADE, 
		related_name='usernames', null = True)
	name = models.CharField(null = True, max_length = 100)
	date = models.DateField(auto_now = True)
	start_time = models.TimeField(auto_now = True)
	finish_time = models.TimeField(null = True)
	total_time = models.TimeField(null = True)
	


