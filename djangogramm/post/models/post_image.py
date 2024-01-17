from django.db import models


class Image(models.Model):
    id = models.AutoField(primary_key=True)

    image = models.ImageField(upload_to="post_image/", blank=True, null=True)

    post = models.ForeignKey(
        "post.Post", on_delete=models.CASCADE, related_name="images"
    )
