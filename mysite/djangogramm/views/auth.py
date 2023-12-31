from django.shortcuts import render
from django.http import HttpResponse

from djangogramm.bl.email_generator import send_confirmation_email
from djangogramm.forms import RegistrationForm


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            email = user.email
            send_confirmation_email(user, email)
            return HttpResponse('Email has been sent, please check your box')
    else:
        form = RegistrationForm()

    return render(request, 'djangogramm/register.html', {"form": form})
