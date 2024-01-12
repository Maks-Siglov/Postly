from django.urls import path

from userprofile import views

app_name = "profile"

urlpatterns = [
    path("profile/<username>", views.profile, name="profile"),
    path(
        "userprofile/<username>/edit", views.edit_profile, name="edit_profile"
    ),
    path(
        "profile_registration/<str:link_key>/",
        views.profile_registration,
        name="profile_registration",
    ),
    path("follow/<int:profile_id>", views.follow, name="follow"),
    path("unfollow/<int:profile_id>", views.unfollow, name="unfollow"),
    path('followers/<int:profile_id>', views.followers, name="followers"),
    path('following/<int:profile_id>', views.following, name="following"),
]
