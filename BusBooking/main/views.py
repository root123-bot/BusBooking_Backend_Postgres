from django.shortcuts import render
from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from BusBooking.passenger.serializers import *
from .models import *
import string, random
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views import View
import datetime

# Create your views here.
class UserDetalsAPIView(APIView):
    def post(self, request, *args, **kwargs):
        
        user_id = request.data.get('user_id')
        print('this is user id ', user_id)
        try:
            user = get_user_model().objects.get(id=int(user_id))
            if hasattr(user, 'passenger'):
                passenger = user.passenger
                serialize = PassengerProfileSerializer(passenger)
                return Response(serialize.data, status=status.HTTP_200_OK)
            
            return Response({"details": "Unrecognized user group" + user_id}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
user_details = UserDetalsAPIView.as_view()

class DeleteUserAPIView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        try:
            user = get_user_model().objects.get(id=int(user_id))
            user.delete()
            return Response({"details": "User deleted successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

delete_user = DeleteUserAPIView.as_view()
