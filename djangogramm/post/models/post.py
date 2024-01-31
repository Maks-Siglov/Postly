from django.contrib.contenttypes.fields import GenericRelation
from django.db import models


class Post(models.Model):
    id = models.AutoField(primary_key=True)

    title = models.CharField(max_length=100)
    content = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    owner = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="posts"
    )

    tags = models.ManyToManyField("post.Tag", related_name="posts")

    likes = GenericRelation("post.Like", related_name="liked_post")
    dislikes = GenericRelation("post.Dislike", related_name="disliked_post")

    class Meta:
        ordering = ("id",)

    def __str__(self):
        return self.title
