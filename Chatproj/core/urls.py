from django.urls import path
from core import views


urlpatterns = [
  path('', views.all_rooms, name = 'index'),
  path('token/', views.token, name="token"),
  path('rooms/<str:slug>/', views.room_detail, name="room_detail"),

]

