import pytest

from django.test.client import Client
from django.urls import reverse

from userprofile.models import UserProfile

from users.models import User


@pytest.mark.django_db
def test_profile(client: Client, test_user_profile):
    user, profile = test_user_profile
    client.login(username="test_user", password="test_password")

    response = client.get(reverse("profile:profile", args=[user.username]))
    assert response.status_code == 200


@pytest.mark.django_db
def test_not_owner_profile_view(client: Client):
    User.objects.create_user(
        username="test_user", password="test_password", email="test@email.com"
    )
    client.login(username="test_user", password="test_password")

    other_user = User.objects.create_user(
        username="other_test_user",
        password="other_test_password",
        email="other@email.com",
    )
    UserProfile.objects.create(user=other_user)
    response = client.get(
        reverse("profile:profile", args=[other_user.username])
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_unauthenticated_profile_view(client: Client):
    response = client.get(reverse("profile:profile", args=["test_user"]))
    assert response.status_code == 302


@pytest.mark.django_db
def test_edit_profile(client: Client, test_user_profile):
    user, profile = test_user_profile
    client.login(username="test_user", password="test_password")

    response_get = client.get(
        reverse("profile:edit_profile", args=[user.username])
    )
    assert response_get.status_code == 200

    response_post = client.post(
        reverse("profile:edit_profile", args=[user.username]),
        data={
            "full_name": "edit_full_name",
            "bio": "edit_bio",
        },
    )
    assert response_post.status_code == 302

    edited_profile = UserProfile.objects.get(user=user)
    assert edited_profile.full_name == "edit_full_name"
    assert edited_profile.bio == "edit_bio"


@pytest.mark.django_db
def test_follow(client: Client, test_user_profile):
    user, profile = test_user_profile

    second_user = User.objects.create_user(
        username="second_test_user",
        password="second_test_password",
        email="second@email.com",
    )
    second_profile = UserProfile.objects.create(
        full_name="second_full_name", bio="second_bio", user=second_user
    )

    client.login(username="test_user", password="test_password")

    response = client.get(reverse("profile:follow", args=[second_profile.id]))
    assert response.status_code == 302
    assert second_profile.followers.all()[0].follower_id == profile.id

    response = client.get(
        reverse("profile:unfollow", args=[second_profile.id])
    )
    assert response.status_code == 302
    assert second_profile.followers.first() is None
