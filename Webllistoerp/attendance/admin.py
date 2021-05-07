from django.contrib import admin
from .models import AttendanceModel, AttendanceData, DatewiseData


admin.site.register(AttendanceModel)

admin.site.register(AttendanceData)

admin.site.register(DatewiseData)