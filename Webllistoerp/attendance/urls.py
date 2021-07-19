from django.contrib import admin
from django.urls import path , include
from django.views.decorators.csrf import csrf_exempt
from attendance import views


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [

  # Attendance URL
  path('attendance/form', views.EmployeeData.as_view(), name = 'attendance-form'),
  path('attendance/info', views.AttendanceInfo.as_view(), name = 'attendance-info'),

  # Leave URL
  path('attendance/dayoff/form', views.DayoffForm.as_view(), name = 'dayoff-form'),
  path('attendance/dayoff/success', views.LeaveFormSuccess.as_view(), name = 'dayoff-form-success'),

  # Notification URL
  path('attendance/notifications_page', views.NotificationsPage.as_view(), name = 'notifications_page'),
  path('not/read/<int:id1>/', views.DeleteNot.as_view(), name = 'make-read'),

  # Holiday and Leave URL
  path('attendance/holidays', views.HolidayDisplay.as_view(), name = 'holidays-page'),
  path('attendance/leave/info', views.LeaveInfo.as_view(), name = 'leave-info'),
  path('attendance/remove-holiday/<int:pk>/', views.RemoveHoliday.as_view(), name = 'remove-holiday'),

  # Timesheet URL
  path('timesheet/record/', views.TimeSheetRecord.as_view(), name = 'timesheet-record'),
  path('timesheet/start/', views.StartTime.as_view(), name = 'start-time'),
  path('timesheet/finish/', views.FinishTime.as_view(), name = 'finish-time'),

  # TL approve path
  path('att/tl/not/<int:id>/', views.TlLeave.as_view(), name = 'tl-leave'),
  path('attendance/tl/approve/<int:id1>/<int:id2>/', views.tl_leave_approve, name = 'tl-approve'),
  path('attendance/tl/not-approve/<int:id1>/<int:id2>/', views.tl_leave_not_approve, name = 'tl-not-approve'),

  # HR approve path
  path('att/hr/not/<int:id1>/', views.HrLeave.as_view(), name = 'hr-leave'),
  path('attendance/approve/hr/<int:id1>/<int:id2>/', views.hr_leave_approve, name = 'hr-approve'),
  path('attendance/hr/not-approve/<int:id1>/<int:id2>/', views.hr_not_approve, name = 'hr-not-approve'),

  # API
  path('api/v1/posts', views.DataCollection.as_view(), name =  'data_collection'),
  path('api/get-data', views.PostCollection.as_view(), name = 'post_collection'),

  # AJAX
  path('attendance/ajax/employee-names/', views.load_names, name = 'employee_load_names'),
  path('attendance/ajax/employee-names-monthly/', views.load_names_monthly, name = 'load_names_monthly'),
  path('att/ajax/timesheet/record/', views.emp_timesheet_record, name = 'emp_timesheet_record'),
]

