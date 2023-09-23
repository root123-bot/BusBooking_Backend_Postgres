from django.db import models
from django.contrib.auth import get_user_model
from BusBooking.main.models import Avatar
# Create your models here.
# in our application user should select avatar from the list of avatars, 
# so we will create a model for avatar so the user will choose only the
# avatar from the list of avatars uploaded by us.. when user created we'll 
# create the profile and we'll 'randomly' pick the avatar from existing avatars
# by randomly taking the avatar id and assigning it to the user profile
# so the first action before doing anything is to have a list of avatars in our database
class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name="passenger")
    avatar = models.OneToOneField(Avatar, on_delete=models.SET_NULL, null=True, blank=True)
    usergroup = models.CharField(max_length=50, default="passenger")
    def __str__(self):
        return self.user.phone_number
    
    # this method will be called when we create the user, so we'll randomly pick the avatar from the list of avatars
    # and assign it to the user profile, we don't need to manually put the logic of picking the avatar, we'll just
    # call this method when we create the user and it will randomly pick the avatar from the list of avatars.
    # this will help to make sure that all users have avatar
    # what is the meaning of .order_by('?')... it means order by random and '?' means random
    def save(self, *args, **kwargs):
        if not self.avatar:
            self.avatar = Avatar.objects.filter(name="default").order_by('?').first()
        super(Profile, self).save(*args, **kwargs)


    @property
    def phone_number(self):
        return self.user.phone_number
    
    @property
    def get_avatar(self):
        return self.avatar.image.url if self.avatar else None
    
    @property
    def get_user_id(self):
        return self.user.id