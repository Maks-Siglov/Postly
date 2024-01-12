from django import template

from users.models import Follow, User

register = template.Library()


@register.filter
def is_following(user: User, following_user: User) -> bool:
    return (Follow.objects.filter(
        follower__id=user.id, following__id=following_user.id
    ).exists())
