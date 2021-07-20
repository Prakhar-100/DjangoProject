from django.db import models

# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
from django.contrib.auth.models import AbstractBaseUser



class CustomUser(models.Model):
	full_name = models.CharField(max_length = 50)
	mobile_no = models.CharField(max_length = 12)

class TOTP(models.Model):
	token = models.CharField(max_length = 6)

	def __str__(self):
		return self.token

class SmsData(models.Model):
	txt = models.CharField(max_length = 500)

	def __str__(self):
		return self.txt
	






# Create your models here.
 # +12254143610

# class ScoreData(models.Model):

# 	score = models.PositiveIntegerField()

# 	def __str__(self):
# 		return str(self.score)

# 	def save(self, *args, **kwargs):
# 		if self.score < 70:
# 			account_sid = 'ACf18711ab713d4b15a1ddc654377761d9'
# 			auth_token = 'cbe252231673c4b318a1903db38fc4a6'
# 			client = Client(account_sid, auth_token)

# 			message = client.messages.create(
# 			         body="Congratulations Prakhar you scored "+str(self.score),
# 			         from_='+12254143610',
# 			         to='+916260336626'
# 			     )

# 			print(message.sid)
# 		return super().save(*args, **kwargs)
