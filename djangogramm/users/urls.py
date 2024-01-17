from django.contrib.auth.views import LogoutView, PasswordResetConfirmView
from django.urls import path, reverse_lazy

from users import views

app_name = "users"

urlpatterns = [
    path("register/", views.registration, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("forgot_password/", views.forgot_password, name="forgot_password"),
    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="users/reset_password.html",
            success_url=reverse_lazy("users:login"),
        ),
        name="password_reset_confirm",
    ),
]
