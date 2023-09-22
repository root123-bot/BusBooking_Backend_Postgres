from rest_framework.serializers import ModelSerializer
from .models import *

# what is depth? can you explain it in detail? 
# depth is used to serialize the foreign key fields of a model.
class PassengerProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'id',
            'get_avatar',
            'phone_number',
            'usergroup',
            'get_user_id'
        ]
