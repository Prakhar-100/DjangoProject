
from django.conf import settings
from django.core.mail import send_mail
from attendance.models import HolidayData
from core.models import CustomUser
from notifications.signals import notify
import datetime
import time
import calendar





def send_mail_of_holiday(occa):
	subject = 'Holiday Alert'
	message = """ On occassion of """+occa+ """ there is holiday tomorrow .
	     Let your client's be informed. Have a good time , """+occa+""" to all
	     in advance.
	     """
	email_from = settings.EMAIL_HOST_USER
	recipient_list = ["anushtha.shree321@gmail.com", "alban.shhai32@gmail.com"]
	send_mail(subject, message, email_from, recipient_list)

def send_notification_of_holiday(occa):
	recp2 = list(CustomUser.objects.all())
	# recp2 = CustomUser.objects.get(email = 'anushtha.shree321@gmail.com')
	sender = CustomUser.objects.get(email = 'piyush_singh@gmail.com')
	data = """ On occassion of """+occa+ """ there is holiday tomorrow piyush_singh@gmail.com.
	     Let your client's be informed. Have a good time , """+occa+""" to all
	     in advance.
	     """
	message = "Holiday Notification"
	notify.send(sender = sender, 
	            recipient = recp2, 
	            verb = message, 
	            description = data)

def my_schedule_job():
	
	obj1 = HolidayData.objects.all()
	date1 = datetime.date.today()

	for i in obj1:
		if i.date.day == date1.day + 1:
			if i.date.month == date1.month:
				send_mail_of_holiday(i.occasion)
				send_notification_of_holiday(i.occasion)


from django.core.management.base import BaseCommand
from django.utils import timezone

class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):
    	my_schedule_job()
    	print("MRJ : Custom command executed!")
		