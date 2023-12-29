from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from djangogramm.forms import RegistrationForm, ProfileForm

from djangogramm.bl.email_generator import generate_unique_link


def index(request):
    return render(request, 'djangogramm/index.html')


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            unique_link = generate_unique_link()

            subject = 'Registration Confirmation'
            message = f'hellooo {unique_link}'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [email]

            send_mail(subject, message, from_email, recipient_list)

            return HttpResponse('Email has been sent, please check your box')
    else:
        form = RegistrationForm()

    return render(request, 'djangogramm/register.html', {"form": form})


def profile(request, link_key):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('Profile saved successfully')

    else:
        form = ProfileForm()
    return render(request, 'djangogramm/profile.html', {"form": form})
