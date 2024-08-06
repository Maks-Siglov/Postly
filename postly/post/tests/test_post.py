import pytest

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.test.client import Client
from django.urls import reverse

from post.models import Comment, Dislike, Like, Post

from userprofile.models import UserProfile

from users.models import User


@pytest.mark.django_db
def test_post_list(client: Client):
    response = client.get(reverse("post:post_list"))
    assert response.status_code == 200
    assert "posts" in response.context


@pytest.mark.django_db
def test_following_posts(client: Client):
    user = User.objects.create_user(
        username="test_username",
        password="test_password",
        email="test@email.com",
    )
    UserProfile.objects.create(
        full_name="Test_full_name", bio="Test_bio", user=user
    )
    Post.objects.create(
        title="test_title_post", content="test_content", owner=user
    )
    client.login(username="test_username", password="test_password")

    response = client.get(
        reverse("post:following_posts", args=[user.username])
    )

    assert response.status_code == 200
    assert "posts" in response.context


@pytest.mark.django_db
def test_user_posts(client: Client, test_user_post):
    user, post = test_user_post
    client.login(username="test_username", password="test_password")

    response = client.get(reverse("post:user_posts", args=[user.username]))
    assert response.status_code == 200
    assert "posts" in response.context


@pytest.mark.django_db
def test_other_user_posts(client: Client, test_user_post):
    User.objects.create_user(
        username="my_test_username",
        password="my_test_password",
        email="other@email.com",
    )
    client.login(username="my_test_username", password="my_test_password")

    other_user, post = test_user_post

    response = client.get(
        reverse("post:user_posts", args=[other_user.username])
    )

    assert response.status_code == 200
    assert "posts" in response.context

    assert b"Edit post" not in response.content
    assert b"Delete post" not in response.content


@pytest.mark.django_db
def test_create_post(client: Client):
    user = User.objects.create_user(
        username="test_username",
        password="test_password",
        email="test@email.com",
    )
    client.login(username="test_username", password="test_password")

    response_get = client.get(reverse("post:create_post"))
    assert response_get.status_code == 200

    post_data = {
        "title": "test_title_post",
        "content": "test_content",
        "tags": "test_tag, second_test_tag",
    }
    response_post = client.post(reverse("post:create_post"), post_data)
    assert response_post.status_code == 302

    post = Post.objects.get(title=post_data["title"])
    assert post.owner == user
    assert post.content == post_data["content"]
    tag = post.tags.all()[0]
    assert tag.name == post_data["tags"].split(",")[0]


@pytest.mark.django_db
def test_post_detail(client: Client, test_user_post):
    user, post = test_user_post
    client.login(username="test_username", password="test_password")

    response_get = client.get(reverse("post:post_detail", args=[post.id]))
    assert response_get.status_code == 200

    post_comment_data = {"content": "my_test_comment"}
    response_post = client.post(
        reverse("post:post_detail", args=[post.id]), post_comment_data
    )
    assert response_post.status_code == 302
    assert post.comments.count() == 1
    comment = post.comments.first()
    assert comment.content == post_comment_data["content"]


@pytest.mark.django_db
def test_edit_post(client: Client, test_user_post):
    user, post = test_user_post
    client.login(username="test_username", password="test_password")

    response_get = client.get(reverse("post:edit_post", args=[post.id]))
    assert response_get.status_code == 200

    edit_post_data = {
        "title": "edit_test_title_post",
        "content": "edit_test_content",
        "tags": "edit_test_tag, second_edit_test_tag",
    }
    response_post = client.post(
        reverse("post:edit_post", args=[post.id]), edit_post_data
    )
    assert response_post.status_code == 302
    edited_post = Post.objects.get(id=post.id)
    assert edited_post.title == edit_post_data["title"]
    assert edited_post.content == edit_post_data["content"]
    tag = edited_post.tags.all()[0]
    assert tag.name == edit_post_data["tags"].split(", ")[0]


@pytest.mark.django_db
def test_not_owner_edit(client: Client, test_user_post):
    user, post = test_user_post
    response_get = client.get(reverse("post:edit_post", args=[post.id]))
    assert response_get.status_code == 302


@pytest.mark.django_db
def test_delete_post(client: Client, test_user_post):
    user, post = test_user_post
    client.login(username="test_username", password="test_password")

    response_get = client.get(reverse("post:delete_post", args=[post.id]))
    assert response_get.status_code == 200

    response_post = client.post(reverse("post:delete_post", args=[post.id]))
    assert response_post.status_code == 302

    with pytest.raises(ObjectDoesNotExist):
        post.refresh_from_db()


@pytest.mark.django_db
def test_not_owner_delete(client: Client, test_user_post):
    user, post = test_user_post
    response_get = client.get(reverse("post:delete_post", args=[post.id]))
    assert response_get.status_code == 302


@pytest.mark.django_db
def test_post_like(client: Client, test_user_post):
    user, post = test_user_post
    client.login(username="test_username", password="test_password")

    response = client.get(reverse("post:like_post", args=[post.id]))
    assert response.status_code == 200

    like_content_type = ContentType.objects.get_for_model(Post)
    like = Like.objects.get(content_type=like_content_type, owner=user)
    assert like

    response = client.get(reverse("post:like_post", args=[post.id]))
    with pytest.raises(ObjectDoesNotExist):
        Like.objects.get(content_type=like_content_type, owner=user)


@pytest.mark.django_db
def test_post_dislike(client: Client, test_user_post):
    user, post = test_user_post
    client.login(username="test_username", password="test_password")

    response = client.get(reverse("post:dislike_post", args=[post.id]))
    assert response.status_code == 200

    like_content_type = ContentType.objects.get_for_model(Post)
    dislike = Dislike.objects.get(content_type=like_content_type, owner=user)
    assert dislike

    response = client.get(reverse("post:dislike_post", args=[post.id]))
    with pytest.raises(ObjectDoesNotExist):
        Dislike.objects.get(content_type=like_content_type, owner=user)


@pytest.mark.django_db
def test_comment_like(client: Client, test_user_post_comment):
    user, post, comment = test_user_post_comment
    client.login(username="test_username", password="test_password")

    response = client.get(reverse("post:like_comment", args=[comment.id]))
    assert response.status_code == 200

    like_content_type = ContentType.objects.get_for_model(Comment)
    like = Like.objects.get(content_type=like_content_type, owner=user)
    assert like

    response = client.get(reverse("post:like_comment", args=[comment.id]))
    with pytest.raises(ObjectDoesNotExist):
        Dislike.objects.get(content_type=like_content_type, owner=user)


@pytest.mark.django_db
def test_comment_dislike(client: Client, test_user_post_comment):
    user, post, comment = test_user_post_comment
    client.login(username="test_username", password="test_password")

    response = client.get(reverse("post:dislike_comment", args=[comment.id]))
    assert response.status_code == 200

    like_content_type = ContentType.objects.get_for_model(Comment)
    dislike = Dislike.objects.get(content_type=like_content_type, owner=user)
    assert dislike

    response = client.get(reverse("post:dislike_comment", args=[comment.id]))
    with pytest.raises(ObjectDoesNotExist):
        Dislike.objects.get(content_type=like_content_type, owner=user)


@pytest.mark.django_db
def test_edit_comment(client: Client, test_user_post_comment):
    user, post, comment = test_user_post_comment
    client.login(username="test_username", password="test_password")

    response = client.get(reverse("post:edit_comment", args=[comment.id]))
    assert response.status_code == 200

    edit_comment_data = {"content": "test_edited_content"}

    response = client.post(
        reverse("post:edit_comment", args=[comment.id]), edit_comment_data
    )
    assert response.status_code == 302

    edited_comment = Comment.objects.get(id=comment.id)
    assert edited_comment.content == edit_comment_data["content"]


@pytest.mark.django_db
def test_delete_comment(client: Client, test_user_post_comment):
    user, post, comment = test_user_post_comment
    client.login(username="test_username", password="test_password")

    response = client.post(reverse("post:delete_comment", args=[comment.id]))
    assert response.status_code == 302

    assert not Comment.objects.filter(id=comment.id).exists()
