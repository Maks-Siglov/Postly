from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    full_name = models.CharField(max_length=255)
    bio = models.TextField()
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
