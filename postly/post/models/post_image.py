from django.db import models


class Image(models.Model):

    image = models.ImageField(upload_to="post_image/", blank=True, null=True)

    post = models.ForeignKey(
        "post.Post", on_delete=models.CASCADE, related_name="images"
    )
