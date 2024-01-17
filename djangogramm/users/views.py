from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import redirect, render

from djangogramm import settings
from users.bl.confirmation_email import send_confirmation_email
from users.forms import RegisterForm, LoginForm, UserForgotPasswordForm


def registration(request) -> HttpResponse:
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            email = user.email
            send_confirmation_email(user, email)
            return render(request, "users/registration_success.html")
    else:
        form = RegisterForm()

    return render(request, "users/register.html", {"form": form})


def login_view(request) -> HttpResponse:
    if request.method == "POST":
        form = LoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("profile:profile", user.username)

            form.add_error(None, "Invalid login credentials")
    else:
        form = LoginForm()

    return render(request, "users/login.html", {"form": form})


def forgot_password(request) -> HttpResponse:
    if request.method == "POST":
        form = UserForgotPasswordForm(request.POST)
        if form.is_valid():
            form.save(request=request, from_email=settings.DEFAULT_FROM_EMAIL)
            messages.success(
                request, "We sent you an email to reset your password"
            )

    else:
        form = UserForgotPasswordForm()
    return render(request, "users/forgot_password.html", {"form": form})
