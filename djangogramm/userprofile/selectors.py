from userprofile.models import UserProfile


def get_followers(profile_id: int) -> list[UserProfile]:
    user_profile = UserProfile.objects.get(id=profile_id)

    follower_ids_list = list(
        user_profile.followers.all().values_list("follower__id", flat=True)
    )
    return UserProfile.objects.filter(id__in=follower_ids_list).all()


def get_following(profile_id: int) -> list[UserProfile]:
    user_profile = UserProfile.objects.get(id=profile_id)

    following_id_list = list(
        user_profile.following.all().values_list("following__id", flat=True)
    )
    return UserProfile.objects.filter(id__in=following_id_list).all()
