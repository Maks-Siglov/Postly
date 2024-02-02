from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    activate_profile = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
