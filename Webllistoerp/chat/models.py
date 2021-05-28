from django.db import models

# Create your models here.

class TextMessage(models.Model):
	e_id      = models.IntegerField()
	e_name    = models.CharField(max_length = 100)
	e_message = models.TextField()
	e_time    = models.TimeField(auto_now=True)

