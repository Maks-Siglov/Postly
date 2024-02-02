import pytest

from users.models import User
from userprofile.models import UserProfile


@pytest.fixture
def test_user_profile(db):
    user = User.objects.create_user(
        username="test_user",
        password="test_password",
        activate_profile=True,
        email="test@email.com"
    )
    profile = UserProfile.objects.create(
        full_name="Test_full_name", bio="Test_bio", user=user
    )
    yield user, profile

    user.delete()
    profile.delete()
