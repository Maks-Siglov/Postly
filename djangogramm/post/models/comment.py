from django.db import models


class Comment(models.Model):
    id = models.AutoField(primary_key=True)

    content = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)

    post = models.ForeignKey(
        "post.Post", on_delete=models.CASCADE, related_name="comments"
    )

    owner = models.ForeignKey(
        "my_auth.User", on_delete=models.CASCADE, related_name="comments"
    )

    likes = models.ManyToManyField(
        "my_auth.User",
        related_name="liked_comments",
    )

    dislikes = models.ManyToManyField(
        "my_auth.User",
        related_name="disliked_comments",
    )
