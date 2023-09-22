from django.shortcuts import render

from BusBooking.main.models import DeviceAuthModel
from .models import *
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from BusBooking.utils.index import sendOTP
from BusBooking.main.models import *
from django.contrib.auth import authenticate
from django.db import IntegrityError
from rest_framework.views import APIView
from BusBooking.passenger.serializers import *
from BusBooking.passenger.models import *
import random
# Create your views here.


def generateOTP():
    OTP = []
    for i in range(4):
        OTP.append(str(random.randint(0, 9)))
    return "".join(OTP)

class IsUserExist(APIView):
    def post(self ,request):
        phone = request.data.get("phone")
        User = get_user_model()
        user = User.objects.filter(phone_number=phone)
        if user.count() > 0:
            return Response({
                "message": "User exist",
                "user_id": user.last().id,
                "user_group": "customer" if hasattr(user.last(), "customer") else "kibanda",
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "message": "User does not exist"
            }, status=status.HTTP_200_OK)
        
is_user_exist = IsUserExist.as_view()


class ValidateOTPAPIView(APIView):
    def post(self, request):
        try:
            phone = request.data.get('phone_number')
            OTP = request.data.get('otp')
            print("RECEIVED OTP ", OTP, phone)
            userOTP = UserOTP.objects.filter(phone=phone, otp=OTP)
            if userOTP.count() > 0:
                userOTP = userOTP.first()
                userOTP.alreadyUsed = True
                userOTP.save()

                # then allow the user to set the new pin where we'll store it in our auth user model and we'll create a new user
                return Response({
                    "message": "OTP validated successfully"
                }, status=status.HTTP_200_OK)
            
            else:
                return Response({
                    "message": "Invalid OTP"
                }, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

validate_otp = ValidateOTPAPIView.as_view()        

class GenerateOTPAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            phone = request.data.get('phone_number')
            OTP = generateOTP()
            # store the OTP and phone number in the database
            # check if there is phone number of that ..
            existingOTP = UserOTP.objects.filter(phone=phone)
            if (existingOTP.count() > 0):
                existingOTP = existingOTP.first()
                existingOTP.otp = OTP
                existingOTP.alreadyUsed = False
                existingOTP.save()
            else:
                userOTP = UserOTP.objects.create(
                    phone=phone,
                    otp=OTP
                )
                
                userOTP.save()
            
            # send this message to the user phone number
            message = f"Nambari ya kuthibitisha, {OTP}"
            sendOTP(phone, message)
            print('this is otp... ', OTP)

            return Response({
                "message": "OTP sent successfully",
                "OTP": OTP
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            print("something went wrong ", e)
            return Response({
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        
send_otp = GenerateOTPAPIView.as_view()


class RegisterUserAPIView(APIView):
    def post(self, request):
        phone = request.data.get('phone_number')
        user_group = request.data.get('usergroup')
        pin = request.data.get('pin')
        deviceID = request.data.get('deviceID')
        print(phone, user_group, pin, deviceID)
        try:
            
            if user_group == "passenger":
                # kumbuka hapa tume-omit 'email' but we said its required_fields in our Auth Model let's see if this will work..
                user = get_user_model().objects.create_user(
                    phone_number=phone,
                    password = pin,
                    email="notset@gmail.com"
                )
                passenger = Profile.objects.create(
                    user=user
                )
                user.save()
                passenger.save()

                # at the end lets save the 'deviceID'
                devices = DeviceAuthModel.objects.filter(modelId=deviceID)
                if devices.count() > 0:
                    device = devices.first()
                    device.pin = pin
                    device.save()
                else:
                    device = DeviceAuthModel.objects.create(
                        modelId=deviceID,
                        pin = pin
                    )
                    device.save()

                serialize = PassengerProfileSerializer(passenger)
                return Response(serialize.data , status=status.HTTP_200_OK)

            else:
                return Response({
                    "message": "Invalid user group"
                }, status=status.HTTP_400_BAD_REQUEST)
            
        # hii ita-catch only the IntegrityError(in case of duplicate phone number) but not the other errors
        except IntegrityError as e:
            # this means we user try to add the same phone number twice
            return Response({
                "message": "User already exist"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # that's why we use this except to catch all the other errors
        except Exception as e:
            print(e)
            return Response({
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


register_user = RegisterUserAPIView.as_view()


class LoginAPIView(APIView):
    def post(self, request):
        try:
            print("this is the request data ", request.data)
            phone = request.data.get("phone")
            password = request.data.get("password")

            user = authenticate(request, username=phone, password=password)
            if user is not None:
                # then we have the user..
                # i should get the category of that user to save to return his profile serializer...
                if hasattr(user, "passenger"):
                    passenger = user.passenger
                    serialize = PassengerProfileSerializer(passenger)

                    return Response({
                        "message": "Login successful",
                        "data": serialize.data
                    }, status=status.HTTP_200_OK)

                else:
                    return Response({
                        "message": "Unrecognized user group"
                    }, status=status.HTTP_401_UNAUTHORIZED)
                
            else:
                return Response({
                    "message": "Invalid credentials"
                }, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return Response({
                "message": "Login failed"
            }, status=status.HTTP_400_BAD_REQUEST)


login = LoginAPIView.as_view()            
