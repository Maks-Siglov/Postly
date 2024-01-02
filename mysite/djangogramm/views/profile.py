from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from djangogramm.forms import ProfileForm
from djangogramm.models import User, UserProfile


def profile_registration(request, link_key):
    if request.method == "POST":
        user = User.objects.get(email_hash=link_key)
        user.activate = True
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile_data = form.cleaned_data
            user_profile_data["user"] = user
            user_profile = UserProfile(**user_profile_data)
            user_profile.save()

            login(request, user)
            messages.success(
                request, "Profile saved and user logged in successfully"
            )
            return redirect("profile", user.username)
    else:
        form = ProfileForm()

    return render(
        request,
        "djangogramm/profile/profile_registration.html",
        {"form": form},
    )


@login_required(login_url="login")
def profile(request, username):
    if request.user.username != username:
        messages.error(
            request, "You do not have permission to view this profile."
        )
        return redirect("index")

    user = User.objects.get(username=username)
    form = ProfileForm(instance=user.profile)
    return render(
        request,
        "djangogramm/profile/profile.html",
        {"form": form},
    )


@login_required(login_url="login")
def edit_profile(request, username):
    user = User.objects.get(username=username)

    if request.user.username != username:
        messages.error(
            request, "You do not have permission to view this profile."
        )
        return redirect("index")

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("profile", username=username)
    else:
        form = ProfileForm(instance=user.profile)

    return render(
        request,
        "djangogramm/profile/edit_profile.html",
        {"form": form},
    )
