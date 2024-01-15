from django.contrib.auth.views import LogoutView
from django.urls import path
from django.contrib.auth.views import PasswordResetConfirmView

from users import views

app_name = 'users'

urlpatterns = [
    path("register/", views.registration, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("forgot_password/", views.forgot_password, name="forgot_password"),
]
