from django.contrib import admin
from .models import  GroupMessage, ChatGroupList, OnetoOneMessage
# Register your models here.

admin.site.register(GroupMessage)

admin.site.register(ChatGroupList)

admin.site.register(OnetoOneMessage)

