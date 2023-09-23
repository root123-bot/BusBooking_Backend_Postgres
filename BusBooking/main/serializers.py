from rest_framework.serializers import ModelSerializer
from .models import *

class AvatarSerializer(ModelSerializer):
    class Meta:
        model = Avatar
        fields = [
            'id',
            'get_image'
        ]