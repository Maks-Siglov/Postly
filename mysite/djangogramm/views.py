from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from djangogramm.forms import RegistrationForm, ProfileForm

from djangogramm.bl.email_generator import send_confirmation_email


def index(request):
    return render(request, 'djangogramm/index.html')


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            send_confirmation_email(email)
            return HttpResponse('Email has been sent, please check your box')
    else:
        form = RegistrationForm()

    return render(request, 'djangogramm/register.html', {"form": form})


def profile(request, link_key):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            user_profile = form.save()
            user_profile.save()
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                return HttpResponse(
                    'Profile saved and user logged in successfully'
                )

    else:
        form = ProfileForm()
    return render(request, 'djangogramm/profile.html', {"form": form})
