from django.contrib import admin
from .models import AttendanceModel, AttendanceData, DatewiseData, UserDayoffData, TimeSheetData, HolidayData


admin.site.register(AttendanceModel)

admin.site.register(AttendanceData)

admin.site.register(DatewiseData)

admin.site.register(UserDayoffData)

admin.site.register(TimeSheetData)

admin.site.register(HolidayData)
