from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email_hash = models.CharField(max_length=32, blank=True, null=True)


class UserProfile(models.Model):
    full_name = models.CharField(max_length=255)
    bio = models.TextField()
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile"
    )
