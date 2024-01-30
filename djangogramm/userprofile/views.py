from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils.http import urlsafe_base64_decode

from users.models import User
from userprofile.forms import ProfileForm
from userprofile.models import UserProfile, Follow
from userprofile.selectors import get_followers, get_following


def activate_profile_validation(request, uidb64: str, token: str):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session["uid"] = uid
        messages.success(request, 'Please activate your profile')
        return redirect('profile:activate_profile')

    else:
        messages.error(request, 'This link is invalid or expired.')
        return redirect('post:post_list')


def activate_profile(request) -> HttpResponse | HttpResponseRedirect:
    uid = request.session.get("uid")
    user = User.objects.get(pk=uid)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():

            user_profile = UserProfile(**form.cleaned_data)
            user.profile = user_profile
            user.activate_profile = True
            user_profile.save()
            user.save()

            login(
                request,
                user,
                backend="django.contrib.auth.backends.ModelBackend",
            )
            messages.success(request, "Profile activated")
            return redirect("profile:profile", user.username)
    else:
        form = ProfileForm()

    return render(
        request,
        "userprofile/profile_registration.html",
        {"form": form},
    )


@login_required(login_url="users:login")
def profile(request, username: str) -> HttpResponse | HttpResponseRedirect:
    profile_owner = User.objects.get(username=username)
    if not profile_owner.activate_profile and request.user == profile_owner:
        return redirect("users:confirm_email", profile_owner.email)

    if request.user == profile_owner:
        return render(
            request,
            "userprofile/profile.html",
            {"profile": profile_owner.profile},
        )

    return render(
        request,
        "userprofile/profile_view.html",
        {"profile": profile_owner.profile, "user": profile_owner},
    )


@login_required(login_url="users:login")
def edit_profile(
    request, username: str
) -> HttpResponse | HttpResponseRedirect:
    user = User.objects.get(username=username)

    if request.user != user:
        messages.error(
            request, "You do not have permission to view this userprofile."
        )
        return redirect("post:post_list")

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("profile:profile", username=username)
    else:
        form = ProfileForm(instance=user.profile)

    return render(
        request,
        "userprofile/edit_profile.html",
        {
            "form": form,
            "user": user,
        },
    )


@login_required(login_url="users:login")
def follow(request, profile_id: int) -> HttpResponseRedirect:
    following_profile = UserProfile.objects.get(id=profile_id)
    follower_profile = request.user.profile
    if not follower_profile.following.filter(
        following_id=following_profile.id
    ).exists():
        Follow.objects.create(
            follower=follower_profile, following=following_profile
        )
        messages.success(
            request, f"You are following to {following_profile.full_name}."
        )
    return redirect("profile:profile", following_profile.user.username)


@login_required(login_url="users:login")
def unfollow(request, profile_id: int) -> HttpResponseRedirect:
    unfollowing_profile = UserProfile.objects.get(id=profile_id)
    unfollower_profile = request.user.profile
    follow_obj = unfollower_profile.following.filter(
        following_id=unfollowing_profile.id
    )
    if follow_obj:
        follow_obj.delete()
        messages.error(
            request, f"You are unfollowing {unfollowing_profile.full_name}."
        )

    return redirect("profile:profile", unfollowing_profile.user.username)


@login_required(login_url="users:login")
def followers(request, profile_id: int) -> HttpResponse:
    user_followers = get_followers(profile_id)

    return render(
        request,
        "userprofile/followers_list.html",
        {"user_followers": user_followers},
    )


@login_required(login_url="users:login")
def following(request, profile_id: int) -> HttpResponse:
    following_users = get_following(profile_id)

    return render(
        request,
        "userprofile/following_list.html",
        {"following_users": following_users},
    )
