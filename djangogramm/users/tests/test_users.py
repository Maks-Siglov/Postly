import re
import pytest

from django.core import mail
from django.test import Client
from django.urls import reverse

from users.models import User
from userprofile.models import UserProfile
from django.contrib.auth.hashers import make_password


@pytest.mark.django_db
def test_registration(client: Client):
    response = client.get(reverse("users:register"))
    assert response.status_code == 200

    response = client.post(
        reverse("users:register"),
        {
            "username": "Test_username",
            "email": "new_user@example.com",
            "password1": "test_password",
            "password2": "test_password",
        },
    )
    assert response.status_code == 200

    user = User.objects.get(username="Test_username")
    assert user.email == "new_user@example.com"
    assert user.check_password("test_password")
    assert user.is_active

    assert len(mail.outbox) == 1
    assert mail.outbox[0].subject == "Registration Confirmation"

    re_pattern = re.compile(r"http(s?)://\S+")
    profile_registration_link_pattern = re_pattern.search(mail.outbox[0].body)
    assert profile_registration_link_pattern
    profile_link = profile_registration_link_pattern.group()
    assert profile_link

    response = client.get(profile_link)
    assert response.status_code == 200

    response = client.post(
        profile_link,
        {"full_name": "Test_full_name", "bio": "Test_bio"},
    )

    assert response.status_code == 302

    assert user.profile.full_name == "Test_full_name"
    assert user.profile.bio == "Test_bio"


@pytest.mark.django_db
def test_login(client: Client):
    user = User.objects.create_user(
        username="tes_tuser", password="test_password"
    )
    response = client.post(
        reverse("users:login"),
        {"username": "tes_tuser", "password": "test_password"},
    )

    assert response.status_code == 302
    assert user.is_active


@pytest.mark.django_db
def test_logout(client: Client):
    user = User.objects.create_user(
        username="test_user", password="test_password"
    )
    profile = UserProfile.objects.create(
        full_name="Test_full_name", bio="Test_bio", user=user
    )
    client.login(username="test_user", password="test_password")

    response = client.get(reverse("profile:profile", args=[user.username]))
    assert response.status_code == 200

    response = client.post(reverse("users:logout"))
    assert response.status_code == 302

    response = client.get(reverse("profile:profile", args=[user.username]))
    assert response.status_code == 302
