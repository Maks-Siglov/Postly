import pytest
from django.test.client import Client
from django.urls import reverse

from users.models import User
from userprofile.models import UserProfile


@pytest.mark.django_db
def test_profile(client: Client):
    user = User.objects.create_user(
        username="test_user", password="test_password"
    )
    profile = UserProfile.objects.create(
        full_name="Test_full_name", bio="Test_bio", user=user
    )
    client.login(username="test_user", password="test_password")

    response = client.get(reverse("profile", args=[user.username]))
    assert response.status_code == 200


@pytest.mark.django_db
def test_not_owner_profile_view(client: Client):
    user = User.objects.create_user(
        username="test_user", password="test_password"
    )
    client.login(username="test_user", password="test_password")

    other_user = User.objects.create_user(
        username="other_test_user", password="other_test_password"
    )
    profile = UserProfile.objects.create(
        full_name="other_test_full_name", bio="other_test_bio", user=other_user
    )

    response = client.get(reverse("profile", args=[other_user.username]))
    assert response.status_code == 200


@pytest.mark.django_db
def test_unauthenticated_profile_view(client: Client):
    response = client.get(reverse("profile", args=["test_user"]))
    assert response.status_code == 302


@pytest.mark.django_db
def test_edit_profile(client: Client):
    user = User.objects.create_user(
        username="test_user", password="test_password"
    )
    profile = UserProfile.objects.create(
        full_name="Test_full_name", bio="Test_bio", user=user
    )
    client.login(username="test_user", password="test_password")

    response_get = client.get(reverse("edit_profile", args=[user.username]))
    assert response_get.status_code == 200

    response_post = client.post(
        reverse("edit_profile", args=[user.username]),
        data={
            "full_name": "edit_full_name",
            "bio": "edit_bio",
        },
    )
    assert response_post.status_code == 302

    edited_profile = UserProfile.objects.get(user=user)
    assert edited_profile.full_name == "edit_full_name"
    assert edited_profile.bio == "edit_bio"
