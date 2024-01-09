from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import redirect, render

from users.bl.email_generator import send_confirmation_email
from users.forms import RegistrationForm


def registration(request) -> HttpResponse:
    if request.method == "POST":
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            email = user.email
            send_confirmation_email(user, email)
            return HttpResponse("Email has been sent, please check your box")
    else:
        form = RegistrationForm()

    return render(request, "my_auth/register.html", {"form": form})


def login_view(request) -> HttpResponse:
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("profile", user.username)

            form.add_error(None, "Invalid login credentials")
    else:
        form = AuthenticationForm()

    return render(request, "my_auth/login.html", {"form": form})
