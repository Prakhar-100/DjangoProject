from core import views
from django.urls import path


urlpatterns = [
	path('', views.index, name = 'index'),
	path('verify/', views.verify_index, name = 'verify-form'),
	path('otp-suc/', views.otp_success, name = 'otp-success'),
   
]