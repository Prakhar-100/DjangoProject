from django.db import models
from core.models import CustomUser

# Create your models here.

class GroupMessage(models.Model):
	e_id      = models.IntegerField()
	e_name    = models.CharField(max_length = 100)
	e_message = models.TextField()
	e_time    = models.TimeField(auto_now=True)
	e_groupid = models.IntegerField()

class OnetoOneMessage(models.Model):
	e_id      = models.IntegerField()
	e_name    = models.CharField(max_length = 100)
	e_message = models.TextField()
	e_time    = models.TimeField(auto_now=True)
	e_groupid = models.IntegerField()

class ChatGroupList(models.Model):
	date_created = models.DateField(auto_now = True)
	time_created = models.TimeField(auto_now = True)
	admin_name   = models.CharField(max_length = 100)
	member_name  = models.ManyToManyField(CustomUser)
	group_name   = models.CharField(max_length = 500)
	description  = models.TextField(blank=True, help_text="description of the group")
	mute_notifications = models.BooleanField(default=False, help_text="disable notification if true")
	icon         = models.ImageField(help_text="Group icon", blank=True, upload_to="chartgroup")
