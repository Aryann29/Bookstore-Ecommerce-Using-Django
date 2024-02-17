from django.contrib.auth.models import User 
from django.db import models
import uuid

from base.models import BaseModel


def get_default_avatar():
    return 'avatars/user.png'

class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile') 
    avatar = models.ImageField(upload_to='avatars', null=True, blank=True, default=get_default_avatar)

    is_seller = models.BooleanField(default=False) 
    bio = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
