from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import CustomUser

# from cmdbox.core.models import Profile

# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# def save_user_profile(sender, instance, **kwargs):
#     instance.core.save()

@receiver(post_save, sender = CustomUser)
def at_ending_save(sender, instance, created, **kwargs):
	# import pdb; pdb.set_trace()
	pass
	# if created:
	# 	CustomUser.objects.create(user = instance)
