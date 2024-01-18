import pytest

from post.models import Post, Comment
from users.models import User


@pytest.fixture
def test_user_post(db):
    user = User.objects.create_user(
        username="test_username", password="test_password"
    )
    post = Post.objects.create(
        title="test_title_post", content="test_content", owner=user
    )
    yield user, post

    user.delete()
    post.delete()


@pytest.fixture
def test_user_post_comment(db):
    user = User.objects.create_user(
        username="test_username", password="test_password"
    )
    post = Post.objects.create(
        title="test_title_post", content="test_content", owner=user
    )
    comment = Comment.objects.create(
        content="test_content", post=post, owner=user
    )
    yield user, post, comment

    user.delete()
    post.delete()
    comment.delete()
