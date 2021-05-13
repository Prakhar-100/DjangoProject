from django.contrib import admin
from django.urls import path , include
from django.views.decorators.csrf import csrf_exempt
from .views import (
	Home,
	attendance_data,
	DataCollection,
	PostCollection,
	AttendanceDataViewJson,
  attendance_form,
  load_names,
  load_names_monthly,
  dayoff_form,
  notifications_page,
  tl_leave_approve,
  tl_leave_not_approve,
  hr_leave_approve,
  hr_not_approve,
  holiday_display,
  remove_holiday,
  leave_info,
  tl_leave,
  hr_leave,
  leave_form_success,
  delete_not
	)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
  path('attendance/home', Home.as_view(), name = 'home'),
  path('attendance/form', attendance_data, name = 'attendance-form'),
  path('attendance/info', attendance_form, name = 'attendance-info'),
  path('attendance/dayoff/form', dayoff_form, name = 'dayoff-form'),
  path('attendance/dayoff/success', leave_form_success, name = 'dayoff-form-success'),
  path('attendance/notifications_page', notifications_page, name = 'notifications_page'),
  path('attendance/holidays', holiday_display, name = 'holidays-page'),
  path('attendance/leave/info', leave_info, name = 'leave-info'),
  path('not/read/<int:id1>/<int:id2>/', delete_not, name = 'make-read'),

  # Button Click event
  # TL approve path
  path('att/tl/not/<int:id>/<int:id2>/', tl_leave, name = 'tl-leave'),
  path('attendance/tl/approve/<int:id1>/<int:id2>/', tl_leave_approve, name = 'tl-approve'),
  path('attendance/tl/not-approve/<int:id1>/<int:id2>/', tl_leave_not_approve, name = 'tl-not-approve'),
  path('attendance/remove-holiday/<int:pk>/', remove_holiday, name = 'remove-holiday'),

  # HR approve path
  # path('attendance/hr/notifications')
  path('att/hr/not/<int:id1>/<int:id2>/', hr_leave, name = 'hr-leave'),
  path('attendance/approve/hr/<int:id1>/<int:id2>/', hr_leave_approve, name = 'hr-approve'),
  path('attendance/hr/not-approve/<int:id1>/<int:id2>/', hr_not_approve, name = 'hr-not-approve'),
  

  # API
  path('api/v1/posts', DataCollection.as_view(), name =  'data_collection'),
  path('api/get-data', PostCollection.as_view(), name = 'post_collection'),

  # AJAX
  path('attendance/ajax/employee-names/', load_names, name = 'employee_load_names'),
  path('attendance/ajax/employee-names-monthly/', load_names_monthly, name = 'load_names_monthly'),
  path('attendance/attendance-data-view/', csrf_exempt(AttendanceDataViewJson.as_view()), name = "attendance-view")
]

# leave_approve,
#   leave_not_approve