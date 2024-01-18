from django.db import models


class UserProfile(models.Model):
    id = models.AutoField(primary_key=True)

    full_name = models.CharField(max_length=255)
    bio = models.TextField()
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.OneToOneField(
        "users.User", on_delete=models.CASCADE, related_name="profile"
    )

    class Meta:
        verbose_name = "Profile"
