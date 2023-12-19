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
            'seat_layout',
            'bookings_metadata',
            'bus_lugagge',
            'booking_timeout_to_pay_for_each_cycle',
            'color_metadata'
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
            'booking_timeout_to_pay_for_each_cycle'
        ]

class BusBookingSerializers(ModelSerializer):
    class Meta:
        model = BusBooking
        fields = [
            'id',
            'bookingId',
            'get_user_id',
            'booked_seats',
            'status',
            'time_to_be_deleted_if_its_not_paid',
            'mark_it_deleted',
            'booking_date',
            'get_bustrip',
            'created_at',
            'updated_at',
            'get_bookerinfo',
            'booking_timeout_to_pay_for_each_cycle'
        ]