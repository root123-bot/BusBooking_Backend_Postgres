from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(DeviceAuthModel)
admin.site.register(DeviceNotificationToken)
admin.site.register(Avatar)
admin.site.register(Notification)