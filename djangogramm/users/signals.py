from django.dispatch import receiver
from django.db.models.signals import post_save
from allauth.socialaccount.models import SocialAccount

from users.models import User
from userprofile.models import UserProfile


@receiver(post_save, sender=SocialAccount)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user = User.objects.get(id=instance.user_id)
        pofile = UserProfile.objects.create(user=user, full_name=user.username)
        user.profile = pofile
        user.activate_profile = True
        user.save()
