from django.db import models


class Comment(models.Model):
    id = models.AutoField(primary_key=True)

    content = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)

    post = models.ForeignKey(
        "djangogramm.Post", on_delete=models.CASCADE, related_name="comments"
    )

    owner = models.ForeignKey(
        "djangogramm.User", on_delete=models.CASCADE, related_name="comments"
    )
