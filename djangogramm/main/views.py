from django.http import HttpResponse
from django.shortcuts import render


def index(request) -> HttpResponse:
    # print(request.user.socialaccount_set.exists())
    return render(request, "main/index.html")
