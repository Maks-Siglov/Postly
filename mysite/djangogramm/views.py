from django.shortcuts import render
from django.http import HttpResponse
from djangogramm.forms import RegistrationForm, ProfileForm

from djangogramm.models import UserProfile, User
from djangogramm.bl.email_generator import send_confirmation_email


def index(request):
    return render(request, 'djangogramm/index.html')


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            email = user.email
            send_confirmation_email(user, email)
            return HttpResponse('Email has been sent, please check your box')
    else:
        form = RegistrationForm()

    return render(request, 'djangogramm/register.html', {"form": form})


def profile(request, link_key):
    if request.method == 'POST':
        user = User.objects.get(email_hash=link_key)
        form = ProfileForm(request.POST)
        if form.is_valid():
            user_profile_data = form.cleaned_data
            user_profile_data['user'] = user
            user_profile = UserProfile(**user_profile_data)
            user_profile.save()
            return HttpResponse(
                'Profile saved and user logged in successfully'
            )

    else:
        form = ProfileForm()
    return render(request, 'djangogramm/profile.html', {"form": form})
