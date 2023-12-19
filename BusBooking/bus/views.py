from django.shortcuts import render
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
import json, random, string
from datetime import datetime, timedelta

# Create your views here.
class AllTrips(APIView):
    def get(self, request):
        try:
            trips = BusTrip.objects.all()
            serialize = BusTripSerializers(trips, many=True)
            return Response(serialize.data, status=status.HTTP_200_OK)
    
        except Exception as e:
            print("eror ", str(e))
            return Response({"details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
all_trips = AllTrips.as_view()

# BEFORE WE CREATE BOOKING LETS CHECK IF THE SEATS IS STILL AVAILABLE..
class CreateBusBooking(APIView):
    def post(self, request):
        try: 
            user_id = request.data.get('user_id')
            bus_id = request.data.get('bus_id')
            seats = request.data.get('seats') # here we've seats labels array stringified 
            trip_id = request.data.get("bustrip")
        
            booking_date = request.data.get('booking_date')

            user = get_user_model().objects.get(id=int(user_id))
            bus = BusInfo.objects.get(id=int(bus_id))

            bustrip = BusTrip.objects.get(id=int(trip_id))
            # check if seat is not already booked..
            # kuna uwezekano kweli tarehe ya booking kuwa nyingi, Yes
            # bustrip can change, Yes? So what we can we can use for it 
            # to be unique, maybe lets add seats..
            # I THINK TRIP IS WHAT MAKE IT UNIQUE AND EASY TO GET ALSO 
            # IN TRIP IS WHAT WE HAVE THE TIME FOR DEPARTURE SO ITS WILL
            # BE UNIQUE, BOOKING_DATE ITS OKAY, SO I EXPECT HERE TO HAVE 
            # ONLY ONE BOOKING... IF THERE ARE MORE THAN ONE BOOKING CALL IT
            # bug
            bookings = BusBooking.objects.filter(
                bus=bus,
                booking_date__exact=datetime.today().date(),
                bustrip = bustrip
            )
            print("PASSED 2")
            print("Bookings ", bookings)
            if (bookings.count() > 1):
                # call it bug, everytime someone book ticket the new booking is created
                # what we should care here is to iterate or get only seats from those bookings...

                already_occupied_seats = []
                for booking in bookings:
                    if json.dumps(already_occupied_seats) == seats:
                        break

                    booked_seats = booking.seats.all()
                    seat_labels = []
                    for bs in booked_seats:
                        seat_labels.append(
                            bs.seat_info.seat_label
                        )
                    incoming_seats = json.loads(seats)

                    for incoming in incoming_seats:
                        if incoming in seat_labels:
                          
                            already_occupied_seats.append(incoming)

                if len(already_occupied_seats) > 0:
                    occupied_seats_str = ", ".join(already_occupied_seats)
                    return Response({
                        "details": f"The seat(s) of label => ({occupied_seats_str}) <= has been occupied"
                    }, status=status.HTTP_409_CONFLICT)


            if (bookings.count() == 1):
                # check booked seats on that bus
                booking = bookings[0]
                booked_seats = booking.seats.all()
                seat_labels = []
                for bs in booked_seats:
                    seat_labels.append(
                        bs.seat_info.seat_label
                    )
                # we have the seat labels
                incoming_seats = json.loads(seats)
                already_occupied_seats = []
                for incoming in incoming_seats:
                    if incoming in seat_labels:
                        # then push it to already_occupied_seat
                        already_occupied_seats.append(incoming)

                if len(already_occupied_seats) > 0:
                    print('SEAT ALREADY BOOKED ', already_occupied_seats)
                    # then push error that seats has already been occupied
                    occupied_seats_str = ", ".join(already_occupied_seats)
                    return Response({
                        "details": f"The seat of label(s) => ({occupied_seats_str}) <= has been occupied"
                    }, status=status.HTTP_409_CONFLICT)

            # we're safe if bookings is empty

            booking_id = ''
            existing_bookingIds = BusBooking.objects.values_list('bookingId', flat=True)
            existing_bookingIds = list(existing_bookingIds)

            flag = True
            while flag:
                booking_id = "".join(random.choices(string.ascii_uppercase + string.digits, k=25))

                if booking_id not in existing_bookingIds:
                    flag = False


            # after 60 minutes this ticket if its still not paid we need to delete it...
            # i will send booking date in this way 'Oct 21 2023'
            # programiz.com/python-programming/datetime/strptime
            '''
                This is how i converted it to actual obj 
                    >>> date_string = 'Oct 21 2023'
                    >>> do = datetime.strptime(date_string, "%b %d %Y")
                    >>> do
                    datetime.datetime(2023, 10, 21, 0, 0)
            '''
            booking = BusBooking.objects.create(
                bus = bus,
                bookingId = booking_id,
                user = user,
                time_to_be_deleted_if_its_not_paid = datetime.now() + timedelta(hours=1),
                booking_date = datetime.strptime(booking_date, "%b %d %Y").date(),
                bustrip = bustrip
            )

            for seat in json.loads(seats):
                bus_seat = BusSeat.objects.create(
                    bus = bus,
                    seat_label = seat
                )
                seat = BookedSeat.objects.create(
                    booked_by=user, 
                    seat_info = bus_seat
                )

                bus_seat.save()
                seat.save()
                booking.seats.add(seat)

            booking.save()
            serializer = BusBookingSerializers(booking)
            return Response(serializer.data, status=status.HTTP_200_OK)


        except Exception as err:
            print("Error occured ", str(err))
            return Response({
                "details": str(err),
            }, status=status.HTTP_400_BAD_REQUEST)
        
create_booking = CreateBusBooking.as_view()

class DeleteBooking(APIView):
    def post(self, request, *args, **kwargs):
        try:
            booking_id = request.data.get('booking_id')
            booking = BusBooking.objects.get(id=int(booking_id))
            booking.delete()

            return Response({
                "details": "Booking deleted successful"
            }, status=status.HTTP_200_OK)
        
        except Exception as err:
            print('Something went wrong ', str(err))
            return Response({
                "details": str(err)
            }, status=status.HTTP_400_BAD_REQUEST)
        
delete_booking = DeleteBooking.as_view()

