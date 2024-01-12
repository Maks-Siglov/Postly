from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class LikeManager(models.Manager):
    def likes(
            self, content_model: models.Model, object_id: int
    ) -> models.QuerySet:
        return super().get_queryset().filter(
            value=True,
            content_type=ContentType.objects.get_for_model(content_model),
            object_id=object_id,
        )

    def dislikes(
            self, content_model: models.Model, object_id: int
    ) -> models.QuerySet:
        return super().get_queryset().filter(
            value=False,
            content_type=ContentType.objects.get_for_model(content_model),
            object_id=object_id,
        )


class Like(models.Model):
    id = models.AutoField(primary_key=True)

    value = models.BooleanField(null=True, blank=True)
    created_auto = models.DateTimeField(auto_now_add=True)
    updated_auto = models.DateTimeField(auto_now=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    owner = models.ForeignKey(
        'users.User', on_delete=models.SET_NULL, null=True
    )

    objects = LikeManager()
