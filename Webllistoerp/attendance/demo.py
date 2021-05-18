#!/home/dell/my_env/bin/python3 -tt
from django_cron import CronJobBase, Schedule
from notifications.signals import notify
from django.conf import settings
from django.core.mail import send_mail
from .models import HolidayData
from core.models import CustomUser
import datetime
import time
import calendar


class MyCronJob(CronJobBase):

	code = 'my_app.my_cron_job'


	def do(self):
		obj1 = HolidayData.objects.all()
		date1 = datetime.date.today()

		for i in obj1:
			if i.date.day == date1.day + 1:

				subject = 'Holiday Alert'
				message = """ On occassion of """+i.occassion+ """ there is holiday tomorrow .
         						Let your client's be informed. Have a good time , """+i.occassion+""" to all
         						in advance."""
				email_from = settings.EMAIL_HOST_USER
				recipient_list = ["anushtha.shree321@gmail.com", "alban.shhai32@gmail.com"]
				send_mail(subject, message, email_from, recipient_list)


				recp2 = CustomUser.objects.all()
				sender = CustomUser.objects.get(designation = 'Director')
				data = """ On occassion of """+i.occassion+ """ there is holiday tomorrow .
									Let your client's be informed. Have a good time , """+i.occassion+""" to all
									in advance."""
				message = "Holiday Notification"

				notify.send(sender = sender, 
							recipient = recp2, 
							verb = message, 
							description = data)



# RUN_EVERY_MINS = 1
    # every 2 hours

    # schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    # code = 'my_app.my_cron_job'