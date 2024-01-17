from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render

from users.models import User
from userprofile.forms import ProfileForm
from userprofile.models import UserProfile, Follow


def activate_profile(
    request, link_key: str
) -> HttpResponse | HttpResponseRedirect:
    if request.method == "POST":
        user = User.objects.get(email_hash=link_key)
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user.activate_profile = True

            user_profile = UserProfile(**form.cleaned_data)
            user.profile = user_profile
            user_profile.save()
            user.save()

            login(
                request,
                user,
                backend="django.contrib.auth.backends.ModelBackend"
            )
            messages.success(
                request, "Profile saved and user logged in successfully"
            )
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

    if not profile_owner.activate_profile:
        return render(request, "userprofile/check_email.html")

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


def create_profile(
        request, username: str
) -> HttpResponse | HttpResponseRedirect:
    user = User.objects.get(username=username)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user.activate_profile = True

            user_profile = UserProfile(**form.cleaned_data)
            user.profile = user_profile
            user_profile.save()
            user.save()

            return redirect("profile:profile", username)
    else:
        form = ProfileForm()

    return render(request, 'userprofile/create_profile.html', {"form": form})


@login_required(login_url="users:login")
def edit_profile(
    request, username: str
) -> HttpResponse | HttpResponseRedirect:
    user = User.objects.get(username=username)

    if request.user != user:
        messages.error(
            request, "You do not have permission to view this userprofile."
        )
        return redirect("main:index")

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
        {"form": form},
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
    user_profile = UserProfile.objects.get(id=profile_id)

    follower_ids_list = list(
        user_profile.followers.all().values_list('follower__id', flat=True)
    )
    user_followers = UserProfile.objects.filter(id__in=follower_ids_list).all()

    return render(
        request,
        "userprofile/followers_list.html",
        {"user_followers": user_followers}
    )


@login_required(login_url="users:login")
def following(request, profile_id: int) -> HttpResponse:
    user_profile = UserProfile.objects.get(id=profile_id)

    following_id_list = list(
        user_profile.following.all().values_list('following__id', flat=True)
    )
    following_users = UserProfile.objects.filter(
        id__in=following_id_list
    ).all()
    return render(
        request,
        "userprofile/following_list.html",
        {"following_users": following_users},
    )
