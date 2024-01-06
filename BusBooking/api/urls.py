from django.urls import path
from django.conf.urls import url
from BusBooking.register.views import *
from django.views.generic import TemplateView
from BusBooking.main.views import *
from BusBooking.bus.views import *

urlpatterns = [
    url(r'clearallnotificationofuser/$', clear_all_notification_of_user, name='clearallnotificationbyuser'),
    url(r'marknotificationdeleted/$', mark_notification_deleted, name='marknotificationdeleted'),
    url(r'fetchnotificationofuser/$', fetch_notification_of_user, name='fetchnotificationofuser'),
    url(r'savedevicenotificationtoken', save_device_notification_token, name='save_device_notification_token'),
    url(r'customerbookings/$', customer_bookings, name='customerbookings'),
    url(r'deletebooking/$', delete_booking, name="deletebooking"),
    url(r'createbooking/$', create_booking, name="createbooking"),
    url(r'alltrips/$', all_trips, name='bustrips'),
    url(r'updateavatar/$', update_avatar, name="updateavatar"),
    url(r'resetpin/$', reset_pin, name='resetpin'),
    url(r'avatars/$', avatars, name='avatars'),
    url(r'delete_user/$', delete_user, name='delete_user'),
    url(r'userdetails/$', user_details, name='login_user'),
    url(r'login/$', login, name='login_user'),
    url(r'register/$', register_user, name='register_user'),
    url(r'isuserexist/$', is_user_exist, name='isuserexist'),
    url(r'sendotp/$', send_otp, name="sendotp"),
    url(r'validateotp/$', validate_otp, name='validateotp'),
]
