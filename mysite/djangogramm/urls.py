from django.contrib.auth.views import LogoutView
from django.urls import path

from djangogramm.views import auth, main_page, post, profile

urlpatterns = [
    path("", main_page.index, name="index"),
]

urlpatterns += [
    path("register/", auth.registration, name="register"),
    path("login/", auth.login_view, name="login"),
    path(
        "profile_registration/<str:link_key>/",
        profile.profile_registration,
        name="profile_registration",
    ),
    path('logout/', LogoutView.as_view(), name='logout')
]

urlpatterns += [
    path("profile/<username>", profile.profile, name="profile"),
    path("profile/<username>/edit", profile.edit_profile, name="edit_profile"),
]


urlpatterns += [
    path("create_post/", post.create_post, name="create_post"),
    path("post_list/", post.post_list, name="post_list"),
    path("post_list/<username>", post.user_posts, name="user_posts"),
    path("post_detail/<int:post_id>", post.post_detail, name="post_detail"),
    path("post/<int:post_id>/edit", post.edit_post, name="edit_post"),
    path("post/<int:post_id>/delete", post.delete_post, name="delete_post"),
    path("like_post/<int:post_id>", post.like_post, name="like_post"),
    path("dislike_post/<int:post_id>", post.dislike_post, name="dislike_post"),
]

urlpatterns += [
    path(
        "like_comment/<int:comment_id>",
        post.like_comment,
        name="like_comment",
    ),
    path(
        "dislike_comment/<int:comment_id>",
        post.dislike_comment,
        name="dislike_comment",
    ),
]
