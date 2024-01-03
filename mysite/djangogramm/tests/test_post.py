import pytest

from django.urls import reverse
from django.test.client import Client

from djangogramm.models import User, Post


@pytest.mark.django_db
def test_post_list(client: Client):
    response = client.get(reverse("post_list"))
    assert response.status_code == 200
    assert "posts" in response.context


@pytest.mark.django_db
def test_user_posts(client: Client):
    user = User.objects.create_user(
        username="test_username", password="test_password"
    )
    post = Post.objects.create(
        title="test_title_post", content="test_content", owner=user
    )
    client.login(username="test_username", password="test_password")

    response = client.get(reverse("user_posts", args=[user.username]))
    assert response.status_code == 200
    assert "posts" in response.context

    assert b"Edit post" in response.content
    assert b"Delete post" in response.content


@pytest.mark.django_db
def test_other_user_posts(client: Client):
    other_user = User.objects.create_user(
        username="other_test_username", password="other_test_password"
    )
    post = Post.objects.create(
        title="test_title_post", content="test_content", owner=other_user
    )

    response = client.get(reverse("user_posts", args=[other_user.username]))
    assert response.status_code == 200
    assert "posts" in response.context

    assert b"Edit post" not in response.content
    assert b"Delete post" not in response.content


@pytest.mark.django_db
def test_create_post(client: Client):
    user = User.objects.create_user(
        username="test_username", password="test_password"
    )
    client.login(username="test_username", password="test_password")

    response_get = client.get(reverse("create_post"))
    assert response_get.status_code == 200

    post_data = {
        "title": "test_title_post",
        "content": "test_content",
        "tag": "test_tag",
    }
    response_post = client.post(reverse("create_post"), post_data)
    assert response_post.status_code == 302

    post = Post.objects.get(title=post_data["title"])
    assert post.owner == user
    assert post.content == post_data["content"]
    tag = post.tags.all()[0]
    assert tag.name == post_data["tag"]


@pytest.mark.django_db
def test_post_detail(client: Client):
    user = User.objects.create_user(
        username="test_username", password="test_password"
    )
    post = Post.objects.create(
        title="test_title_post", content="test_content", owner=user
    )
    client.login(username="test_username", password="test_password")

    response_get = client.get(reverse("post_detail", args=[post.id]))
    assert response_get.status_code == 200

    post_comment_data = {"content": "my_test_comment"}
    response_post = client.post(
        reverse("post_detail", args=[post.id]), post_comment_data
    )
    assert response_post.status_code == 200
    assert post.comments.count() == 1
    comment = post.comments.first()
    assert comment.content == post_comment_data["content"]


@pytest.mark.django_db
def test_edit_post(client: Client):
    user = User.objects.create_user(
        username="test_username", password="test_password"
    )
    post = Post.objects.create(
        title="test_title_post", content="test_content", owner=user
    )
    client.login(username="test_username", password="test_password")

    response_get = client.get(reverse("edit_post", args=[post.id]))
    assert response_get.status_code == 200

    edit_post_data = {
        "title": "edit_test_title_post",
        "content": "edit_test_content",
        "tag": "edit_test_tag",
    }
    response_post = client.post(
        reverse("edit_post", args=[post.id]), edit_post_data
    )
    assert response_post.status_code == 302
    edited_post = Post.objects.get(id=post.id)
    assert edited_post.title == edit_post_data["title"]
    assert edited_post.content == edit_post_data["content"]
    tag = edited_post.tags.all()[0]
    assert tag.name == edit_post_data["tag"]
