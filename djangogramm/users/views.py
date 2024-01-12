from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.shortcuts import redirect, render

from users.bl.email_generator import send_confirmation_email
from users.forms import RegisterForm, LoginForm


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
        print(make_password("289331qq"))
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
