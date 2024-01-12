from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.AutoField(primary_key=True)

    email_hash = models.CharField(max_length=32, blank=True, null=True)
    activate = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
