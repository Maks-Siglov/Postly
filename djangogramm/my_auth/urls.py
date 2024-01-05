from django.contrib.auth.views import LogoutView
from django.urls import path

from my_auth import views

urlpatterns = [
    path("register/", views.registration, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
