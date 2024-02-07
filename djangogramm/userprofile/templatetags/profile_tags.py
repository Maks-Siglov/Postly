from django import template

from userprofile.models import Follow, UserProfile

register = template.Library()


@register.filter
def is_following(profile: UserProfile, following_profile: UserProfile) -> bool:
    return Follow.objects.filter(
        follower__id=profile.id, following__id=following_profile.id
    ).exists()
