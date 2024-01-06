from django.shortcuts import render
from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from BusBooking.passenger.serializers import *
from BusBooking.main.serializers import *
from BusBooking.main.models import *
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
        # print('this is user id ', user_id)
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

class Avatars(APIView):
    def get(self, request):
        avatars = Avatar.objects.all()
        serialize = AvatarSerializer(avatars, many=True)
        return Response(serialize.data, status=status.HTTP_200_OK)

avatars = Avatars.as_view()

class UpdateProfileAvatar(APIView):
    def post(self, request):
        try: 
            avatar_id = request.data.get('avatar_id')
            user_id = request.data.get('user_id')

            avatar = Avatar.objects.get(id=int(avatar_id))
            user = get_user_model().objects.get(id=int(user_id))

            passenger = user.passenger
            passenger.avatar = avatar
            passenger.save()

            return Response({
                "message": "Success"
            }, status=status.HTTP_200_OK)
        
        except Exception as err:
            return Response({
                "details": str(err)
            }, status=status.HTTP_400_BAD_REQUEST)

update_avatar = UpdateProfileAvatar.as_view()

class SaveDeviceNotificationToken(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        token = request.data.get('token')
        try:
            user = get_user_model().objects.get(id=int(user_id))
            notificationToken = DeviceNotificationToken.objects.filter(user=user)

            if notificationToken.exists():
                notificationToken = notificationToken.first()
                notificationToken.deviceNotificationToken = token
                notificationToken.save()
                return Response({"details": "Token updated successfully"}, status=status.HTTP_200_OK)

            else:
                notificationToken = DeviceNotificationToken.objects.create(user=user, deviceNotificationToken=token)
                notificationToken.save()
                return Response({"details": "Token added successfully"}, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
save_device_notification_token = SaveDeviceNotificationToken.as_view()

class MarkNotificationAsRead(APIView):
    def post(self, request, *args, **kwargs):
        id = request.data.get('notification_id')

        try: 
            notification = Notification.objects.get(id=int(id))

            notification.is_read  = True
            notification.save()
            return Response({
                "message": "Successful",
            }, status=status.HTTP_200_OK)
        
        except Exception as err:
            print("Error ", err)
            return Response(
                {"details": str(err)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
mark_notification_as_read = MarkNotificationAsRead.as_view()

class ClearAllNotificationOfUser(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")
        try:
            user = get_user_model().objects.get(id=int(user_id))
            notifications = Notification.objects.filter(receiver=user, is_deleted=False)
            for notification in notifications:
                notification.is_deleted = True
                notification.is_read = True
                notification.save()
            return Response({"details": "success"}, status=status.HTTP_200_OK)
        except Exception as e:
            print("error ", e)
            return Response({ "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
clear_all_notification_of_user = ClearAllNotificationOfUser.as_view()

class MarkNotificationDeleted(APIView):
    def post(self, request):
        notification_id = request.data.get("notification_id")
        try:
            notification = Notification.objects.get(id=int(notification_id))
            notification.is_deleted = True
            notification.is_read = True
            notification.save()
            serialize = NotificationSerializer(notification)
            return Response(serialize.data, status=status.HTTP_200_OK)
        except Exception as e:
            print("error ", e)
            return Response({ "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
mark_notification_deleted = MarkNotificationDeleted.as_view()

class FetchNotificationOfUser(APIView):
    def post(self, request):
        try:
            user_id = request.data.get("user_id")
            user = get_user_model().objects.get(id=int(user_id))
            print('THE USER ID ', user.id)
            print('NOTIFICATIONS ', Notification.objects.all())
            notifications = Notification.objects.filter(receiver=user, is_deleted=False)
            notifications = reversed(notifications)
            serialize = NotificationSerializer(notifications, many=True)
            return Response(serialize.data, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({ "details": str(err) }, status=status.HTTP_400_BAD_REQUEST)

fetch_notification_of_user = FetchNotificationOfUser.as_view()
