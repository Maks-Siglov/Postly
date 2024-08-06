from django.urls import path

from post import views

app_name = "post"

urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("create_post/", views.create_post, name="create_post"),
    path("post_list/<str:username>", views.user_posts, name="user_posts"),
    path(
        "following_posts/<str:username>",
        views.following_posts,
        name="following_posts",
    ),
    path("post_detail/<int:post_id>", views.post_detail, name="post_detail"),
    path("post/<int:post_id>/edit", views.edit_post, name="edit_post"),
    path("post/<int:post_id>/delete", views.delete_post, name="delete_post"),
    path(
        "comment/<int:comment_id>/delete",
        views.delete_comment,
        name="delete_comment",
    ),
    path(
        "comment/<int:comment_id>/edit",
        views.edit_comment,
        name="edit_comment",
    ),
    path("like_post/<int:post_id>", views.like_post, name="like_post"),
    path(
        "dislike_post/<int:post_id>", views.dislike_post, name="dislike_post"
    ),
    path(
        "like_comment/<int:comment_id>",
        views.like_comment,
        name="like_comment",
    ),
    path(
        "dislike_comment/<int:comment_id>",
        views.dislike_comment,
        name="dislike_comment",
    ),
]
