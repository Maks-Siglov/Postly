from django.contrib.auth import login
from django.shortcuts import render
from django.http import HttpResponse

from djangogramm.forms import ProfileForm
from djangogramm.models import UserProfile, User


def profile(request, link_key):
    if request.method == 'POST':
        user = User.objects.get(email_hash=link_key)
        user.activate = True
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile_data = form.cleaned_data
            user_profile_data['user'] = user
            user_profile = UserProfile(**user_profile_data)
            user_profile.save()

            login(request, user)
            return HttpResponse(
                'Profile saved and user logged in successfully'
            )
    else:
        form = ProfileForm()

    return render(request, 'djangogramm/profile.html', {"form": form})
