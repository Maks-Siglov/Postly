from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils.http import urlsafe_base64_decode

from userprofile.forms import ProfileForm
from userprofile.models import Follow, UserProfile
from userprofile.selectors import get_followers, get_following

from users.models import User


def activate_profile_validation(
    request: HttpRequest, uidb64: str, token: str
) -> HttpResponseRedirect:
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, ObjectDoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session["uid"] = uid
        messages.success(request, "Please activate your profile")
        return redirect("profile:activate_profile")

    else:
        messages.error(request, "This link is invalid or expired.")
        return redirect("post:post_list")


def activate_profile(
    request: HttpRequest,
) -> HttpResponse | HttpResponseRedirect:
    try:
        uid = request.session.get("uid")
        user = User.objects.get(pk=uid)
    except ObjectDoesNotExist:
        messages.error(request, "Error during activating profile")
        return redirect("post:post_list")

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
def profile(
    request: HttpRequest, username: str
) -> HttpResponse | HttpResponseRedirect:
    try:
        profile_owner = User.objects.get(username=username)
    except ObjectDoesNotExist:
        messages.error(request, "This user does not exist")
        return redirect("post:post_list")

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
    request: HttpRequest, username: str
) -> HttpResponse | HttpResponseRedirect:
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        messages.error(request, "Error during reset password")
        return redirect("post:post_list")

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
def follow(request: HttpRequest, profile_id: int) -> HttpResponseRedirect:
    try:
        following_profile = UserProfile.objects.get(id=profile_id)
    except ObjectDoesNotExist:
        messages.error(request, "Following profile does not exist")
        return redirect("post:post_list")

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
def unfollow(request: HttpRequest, profile_id: int) -> HttpResponseRedirect:
    try:
        unfollowing_profile = UserProfile.objects.get(id=profile_id)
    except ObjectDoesNotExist:
        messages.error(request, "Following profile does not exist")
        return redirect("post:post_list")

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
def followers(request: HttpRequest, profile_id: int) -> HttpResponse:
    try:
        user_followers = get_followers(profile_id)
    except ObjectDoesNotExist:
        messages.error(request, f"Profile {profile_id }does not exist")
        return redirect("post:post_list")

    return render(
        request,
        "userprofile/followers_list.html",
        {"user_followers": user_followers},
    )


@login_required(login_url="users:login")
def following(request: HttpRequest, profile_id: int) -> HttpResponse:
    try:
        following_users = get_following(profile_id)
    except ObjectDoesNotExist:
        messages.error(request, f"Profile {profile_id }does not exist")
        return redirect("post:post_list")

    return render(
        request,
        "userprofile/following_list.html",
        {"following_users": following_users},
    )
