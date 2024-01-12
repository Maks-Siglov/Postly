from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib import messages

from userprofile.models import UserProfile
from users.bl.email_generator import send_confirmation_email
from users.forms import RegisterForm, LoginForm
from users.models import Follow


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


def follow(request, profile_id: int):
    following_profile = UserProfile.objects.get(id=profile_id)
    following_user = following_profile.user
    if not request.user.following.filter(
            following_id=following_user.id
    ).exists():
        Follow.objects.create(follower=request.user, following=following_user)
        messages.success(
            request, f"You are following to {following_user.username}."
        )
    return redirect("profile:profile", following_user.username)


def unfollow(request, profile_id: int):
    unfollowing_profile = UserProfile.objects.get(id=profile_id)
    unfollowing_user = unfollowing_profile.user
    follow_obj = request.user.following.filter(
        following_id=unfollowing_user.id
    )
    if follow_obj:
        follow_obj.delete()
        messages.error(
            request, f"You are unfollowing {unfollowing_user.username}."
        )

    return redirect("profile:profile", unfollowing_user.username)
