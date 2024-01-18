from django.db import models


class Follow(models.Model):
    follower = models.ForeignKey(
        "userprofile.UserProfile",
        on_delete=models.SET_NULL,
        related_name="following",
        null=True,
    )
    following = models.ForeignKey(
        "userprofile.UserProfile",
        on_delete=models.CASCADE,
        related_name="followers",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("follower", "following")
