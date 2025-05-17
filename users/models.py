from django.db import models
from django.contrib.auth.models import AbstractUser
from core.models import BaseModel


class CustomUser(AbstractUser, BaseModel):
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=20,
        choices=[
            ('user', 'User'),
            ('admin', 'Admin'),
            ('operator', 'Operator'),
        ],
        default='user'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

class UserProfile(BaseModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.email}'s Profile"