from django.urls import path
from .  import views
# from django.contrib.auth import views


urlpatterns = [
  path('', views.Login1.as_view(), name = 'login1'),
  path('accounts/signup/index/', views.Index.as_view(), name = 'index'),
  path('index/', views.Index.as_view(), name = 'index'),
  # path('index2/', views.index2, name = 'index2'),
  # path('accounts/signup/dashboard/', views.dashboard, name = 'dashboard'),
  path('accounts/signup/', views.Sign_up.as_view(), name = 'sign_up'),
  path(r'^core/datatable/record_delete/(?P<int:member_id>\d+)/$', views.record_delete, name='record_delete'),
  path(r'^core/datatable/record_change/(?P<int:member_id>\d+)/$', views.record_update, name = 'record_change'),
  path('ajax/load-names/', views.load_names, name = 'ajax_load_names'),
  path('accounts/logout/', views.Logout_View.as_view(), name = 'logout_view'),
  # path('ajax/load-names/', views.load_usernames, name = 'ajax_load_usernames'),
  path('core/datatable/', views.datatable, name = 'datatable'),
  path('core/promodel/', views.promodel, name = 'promodel'),
  path('core/designationupdate/', views.designation_update, name = 'designationupdate')
  # path('core/promodel/', views.promodel.as_view(), name = 'promodel')
]