from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from multiselectfield import MultiSelectField

# from django.utils.translation import ugettext_lazy_as_ 
# Create your models here.

class CustomUser(AbstractUser):
    designation = models.CharField(max_length = 50, blank = True)

class UserHeirarchy(models.Model):
    usernm = models.ForeignKey(CustomUser, on_delete = models.CASCADE, related_name='user_name', null = True) 
    child = models.ForeignKey(CustomUser, on_delete = models.CASCADE, related_name='child_name', null = True)
    
    def __str__(self):
        return str(self.usernm)+'  '+str(self.child)


class EmailBackend(object):

    def authenticate(self, request, email=None, password=None, **kwargs):
        # User = get_user_model()
        # User = User.objects.all()
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return None
        else:
            if getattr(user, 'is_active') and user.check_password(password):
                return user
        return None
    def get_user(self, user_id):
        # User = get_user_model()        
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None

