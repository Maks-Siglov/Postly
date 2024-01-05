from django.db import models


class UserProfile(models.Model):
    id = models.AutoField(primary_key=True)

    full_name = models.CharField(max_length=255)
    bio = models.TextField()
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    user = models.OneToOneField(
        "my_auth.User", on_delete=models.CASCADE, related_name="profile"
    )
