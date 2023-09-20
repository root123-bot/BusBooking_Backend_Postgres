from django.urls import path
from django.conf.urls import url
from BusBooking.register.views import *
from django.views.generic import TemplateView
from BusBooking.main.views import *


urlpatterns = [
    url(r'login/$', login, name='login_user'),
    url(r'register/$', register_user, name='register_user'),
    url(r'isuserexist/$', is_user_exist, name='isuserexist'),
    url(r'sendotp/$', send_otp, name="sendotp"),
    url(r'validateotp/$', validate_otp, name='validateotp'),
]
