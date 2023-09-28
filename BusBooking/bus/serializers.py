from rest_framework.serializers import ModelSerializer
from .models import *

class BusInfoSerializers(ModelSerializer):
    class Meta:
        model = BusInfo
        fields = [
            'id',
            'bus_name',
            'bus_number',
            'bus_type',
            'plate_number',
            'created_at',
            'updated_at',
            'bookings_metadata',
        ]

class BusTripSerializers(ModelSerializer):
    class Meta:
        model = BusTrip
        fields = [
            'id',
            'day',
            'bus_source',
            'bus_destination',
            'departure_station',
            'destination_station',
            'bus_departure_time',
            'source_arrival_time',
            'bus_fare',
            'bus_info',
            'destination_arrival_time',
            'created_at',
            'updated_at',
        ]