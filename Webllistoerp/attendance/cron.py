from notifications.signals import notify
from django.conf import settings
from django.core.mail import send_mail
from .models import HolidayData
from core.models import CustomUser
import datetime
import time
import calendar

def send_mail_of_holiday(occassion):
	subject = 'Holiday Alert'
	message = """ On occassion of """+occassion+ """ there is holiday tomorrow .
         Let your client's be informed. Have a good time , """+occassion+""" to all
         in advance.
         """
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ["anushtha.shree321@gmail.com", "alban.shhai32@gmail.com"]
    send_mail(subject, message, email_from, recipient_list)

def send_notification_of_holiday(occassion):
	recp2 = list(CustomUser.objects.all())
	sender = CustomUser.objects.get(designation = 'Director')
	data = """ On occassion of """+occassion+ """ there is holiday tomorrow .
         Let your client's be informed. Have a good time , """+occassion+""" to all
         in advance.
         """
    message = "Holiday Notification"

	notify.send(sender = sender, 
                recipient = recp2, 
                verb = message, 
                description = data)


def my_schedule_job():

	import pdb; pdb.set_trace()
	obj1 = HolidayData.objects.all()
	date1 = datetime.date.today()

	for i in obj1:
		if i.date.day == date1.day + 1:
			send_mail_of_holiday(i.occassion)
			send_notification_of_holiday(i.occassion)
		
        # date_obj1 = datetime.datetime.strptime(request.POST['calen1'], '%Y-%m-%d').date()



# def my_schedule_holiday():
	# with open('demo.txt', 'w+') as f:
	# 	f.write("test line\n")
	obj1 = HolidayData.objects.all()
	date1 = datetime.date.today()

	for i in obj1:
		if i.date.day == date1.day + 1:
			send_mail_of_holiday(i.occassion)
			send_notification_of_holiday(i.occassion)

def test_cronjob():

	if __name__ == '__main__':
		obj1 = HolidayData.objects.all()
		date1 = datetime.date.today()

		for i in obj1:
			if i.date.day == date1.day + 1:
				send_mail_of_holiday(i.occassion)
				send_notification_of_holiday(i.occassion)


