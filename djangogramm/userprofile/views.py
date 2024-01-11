from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render

from users.models import User
from userprofile.forms import ProfileForm
from userprofile.models import UserProfile


def profile_registration(
    request, link_key: str
) -> HttpResponse | HttpResponseRedirect:
    if request.method == "POST":
        user = User.objects.get(email_hash=link_key)
        user.activate = True
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.cleaned_data["user"] = user
            user_profile = UserProfile(**form.cleaned_data)
            user_profile.save()

            login(request, user)
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
def profile(request, username: str) -> HttpResponse:
    profile_owner = User.objects.get(username=username)
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
