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
]

urlpatterns += [
    path("profile/<username>", profile.profile, name="profile"),
    path("profile/<username>/edit", profile.edit_profile, name="edit_profile"),
]


urlpatterns += [
    path("create_post/", post.create_post, name="create_post"),
    path("post_list/", post.post_list, name="post_list"),
    path("post_detail/<int:post_id>", post.post_detail, name="post_detail"),
    path("like_post/<int:post_id>", post.like_post, name="like_post"),
    path("dislike_post/<int:post_id>", post.dislike_post, name="dislike_post"),
]
