from django.contrib.auth.views import LogoutView
from django.urls import path

from users import views

app_name = 'users'

urlpatterns = [
    path("register/", views.registration, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("follow/<int:profile_id>", views.follow, name="follow"),
    path("unfollow/<int:profile_id>", views.unfollow, name="unfollow"),
]
