from django.shortcuts import render, redirect
from django.http import HttpResponse
from djangogramm.forms import RegistrationForm


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            return HttpResponse('')
    else:
        form = RegistrationForm()

    return render(request, 'djangogramm/register.html', {"form": form})
