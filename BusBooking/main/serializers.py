from rest_framework.serializers import ModelSerializer
from .models import *

class AvatarSerializer(ModelSerializer):
    class Meta:
        model = Avatar
        fields = [
            'id',
            'get_image'
        ]


class NotificationSerializer(ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            'id',
            'heading',
            'body',
            'created_at',
            'is_read',
            'is_deleted',
            'get_booking',
            'get_receiver',
            'is_associted_with_booking',
        ]
