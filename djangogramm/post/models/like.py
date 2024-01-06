import uuid

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class LikeManager(models.Manager):
    def likes(self):
        return super().get_queryset().filter(value=True)

    def dislikes(self):
        return super().get_queryset().filter(value=False)


class Like(models.Model):
    id = models.AutoField(primary_key=True)

    value = models.BooleanField(null=True, blank=True)
    created_auto = models.DateTimeField(auto_now_add=True)
    updated_auto = models.DateTimeField(auto_now=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    owner = models.ForeignKey(
        'my_auth.User', on_delete=models.SET_NULL, null=True
    )

    objects = LikeManager()
