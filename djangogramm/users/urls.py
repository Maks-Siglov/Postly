from django.contrib.auth.views import LogoutView
from django.urls import path

from users import views

app_name = "users"

urlpatterns = [
    path("register/", views.registration, name="register"),
    path(
        "confirm_email/<str:email>", views.confirm_email, name="confirm_email"
    ),
    path("login/", views.login_view, name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("forgot_password/", views.forgot_password, name="forgot_password"),
    path(
        "reset_password_validation/<uidb64>/<token>/",
        views.reset_password_validation,
        name="reset_password_validation",
    ),
    path("reset_password/", views.reset_password, name="reset_password"),
    path(
        "resend_verification_email/<str:email>",
        views.resend_verification_email,
        name="resend_verification_email",
    ),
    path("change_email/<str:email>", views.change_email, name="change_email"),
]
