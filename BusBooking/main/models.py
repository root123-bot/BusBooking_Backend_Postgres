from django.db import models
from django.contrib.auth import get_user_model
from BusBooking.bus.models import *
from BusBooking.bus.serializers import *

# Create your models here.

class DeviceAuthModel(models.Model):
    modelId = models.CharField(max_length=255)
    pin = models.CharField(max_length=255)


class DeviceNotificationToken(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name="notificationToken")
    deviceNotificationToken = models.CharField(max_length=255)

class Avatar(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="avatars/")

    @property
    def get_image(self):
        return self.image.url

class Notification(models.Model):
    receiver = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='notifications')
    heading = models.CharField(max_length=255)
    body = models.TextField()    
    is_associated_with_booking = models.BooleanField(default=False)
    booking = models.ForeignKey(BusBooking, on_delete=models.CASCADE, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def get_receiver(self):
        return {
            "id": self.receiver.id,
            "user_id": self.receiver.id,
            "phone": self.receiver.phone_number
        }

    @property
    def get_booking(self):
        booking = None
        if self.booking:
            return {
                "id": self.booking.id,
                "booking_id": self.booking.bookingId,
                "bus": BusInfoSerializers(self.booking.bus),
                "seats": BusSeatSerializers(self.booking.seats.all(), many=True),
                "status": self.booking.status,
                "mark_it_deleted": self.booking.mark_it_deleted,
                "time_to_wait_before_deleting_if_not_paid": self.booking.time_to_be_deleted_if_its_not_paid,
                "booking_date": self.booking.booking_date,
                "bustrip": BusTripSerializers(self.booking.bustrip),
                "created_at": self.booking.created_at,
                "updated_at": self.booking.updated_at,
            }
        return booking
          