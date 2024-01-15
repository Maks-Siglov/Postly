from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import SetPasswordForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render

from users.bl.confirmation_email import send_confirmation_email
from users.bl.reset_password_email import send_resetting_password_email
from users.forms import RegisterForm, LoginForm, EmailForm
from users.models import User


def registration(request) -> HttpResponse:
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            email = user.email
            send_confirmation_email(user, email)
            return render(request, 'users/registration_success.html')
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
        form = EmailForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data["email"]
            user = User.objects.get(email=user_email)

            send_resetting_password_email(user)
            return render(request, "users/forgot_password_email.html")

    else:
        form = EmailForm()
    return render(request, "users/forgot_password.html", {"form": form})


def reset_password(
        request, link_key: str
) -> HttpResponse | HttpResponseRedirect:
    user = User.objects.get(email_hash=link_key)
    if request.method == "POST":
        form = SetPasswordForm(user=user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "You successfully reset your password")
            return redirect("users:login")

    else:
        form = SetPasswordForm(user=user)

    return render(request, "users/reset_password.html", {"form": form})
