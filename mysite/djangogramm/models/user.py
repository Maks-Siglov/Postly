from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    id = models.AutoField(primary_key=True)

    email_hash = models.CharField(max_length=32, blank=True, null=True)
    activate = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)


class UserProfile(models.Model):
    id = models.AutoField(primary_key=True)

    full_name = models.CharField(max_length=255)
    bio = models.TextField()
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile"
    )
