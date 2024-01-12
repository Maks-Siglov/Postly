from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.AutoField(primary_key=True)

    email_hash = models.CharField(max_length=32, blank=True, null=True)
    activate = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)


class Follow(models.Model):
    follower = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        related_name='following',
        null=True,
    )
    following = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='followers',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')
