import pytest
import re

from django.core import mail
from django.urls import reverse
from django.test import Client

from djangogramm.models import User, UserProfile


@pytest.mark.django_db
def test_registration(client: Client):
    response = client.get(reverse("register"))
    assert response.status_code == 200

    response = client.post(
        reverse("register"),
        {
            "username": "Test_username",
            "email": "new_user@example.com",
            "password": "test_password",
        },
    )
    assert response.status_code == 200

    user = User.objects.get(username="Test_username")
    assert user.email == "new_user@example.com"
    assert user.check_password("test_password")
    assert user.is_active

    assert len(mail.outbox) == 1
    assert mail.outbox[0].subject == "Registration Confirmation"

    re_pattern = re.compile(r"http://\S+")
    profile_registration_link_pattern = re_pattern.search(mail.outbox[0].body)
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
        username='tes_tuser', password='test_password'
    )
    response = client.post(
        reverse('login'),
        {'username': 'tes_tuser', 'password': 'test_password'}
    )

    assert response.status_code == 302
    assert user.is_active


@pytest.mark.django_db
def test_logout(client: Client):
    user = User.objects.create_user(
        username='test_user', password='test_password'
    )
    profile = UserProfile.objects.create(
        full_name="Test_full_name", bio="Test_bio", user=user
    )
    client.login(username='test_user', password='test_password')

    response = client.get(reverse('profile',  args=[user.username]))
    assert response.status_code == 200

    response = client.post(reverse('logout'))
    assert response.status_code == 302

    response = client.get(reverse('profile',  args=[user.username]))
    assert response.status_code == 302
