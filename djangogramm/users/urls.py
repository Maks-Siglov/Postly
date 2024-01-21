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
        "reset_password_validation/<uidb64>/<token>/",
        views.reset_password_validation,
        name="reset_password_validation",
    ),
    path('reset_password/', views.reset_password, name="reset_password"),
]
