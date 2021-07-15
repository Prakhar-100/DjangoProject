from django.urls import path
from .  import views
from django.views.decorators.csrf import csrf_exempt
from django.conf.urls.static import static
# from django.contrib.auth import views


urlpatterns = [
  path('', csrf_exempt(views.Login1.as_view()), name = 'login1'),
  path('index/', views.Index.as_view(), name = 'index'),
  path('accounts/signup/', views.Sign_up.as_view(), name = 'sign_up'),
  path('core/promodel/', views.Promodel.as_view(), name = 'promodel'),
  path('core/designationupdate/', views.DesignationUpdate.as_view(), name = 'designationupdate'),

  # Ajax Call
  path('ajax/load-names/', views.load_names, name = 'ajax_load_names'),
]

