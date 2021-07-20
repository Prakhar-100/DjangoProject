from django.contrib import admin
from core.models import CustomUser, TOTP, SmsData
# Register your models here.



admin.site.register(CustomUser)

admin.site.register(TOTP)

admin.site.register(SmsData)