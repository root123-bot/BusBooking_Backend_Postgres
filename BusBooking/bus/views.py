from django.shortcuts import render
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *

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