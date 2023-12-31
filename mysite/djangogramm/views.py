from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse

from djangogramm.bl.email_generator import send_confirmation_email
from djangogramm.forms import RegistrationForm, ProfileForm, PostForm
from djangogramm.models import UserProfile, User, Post


def index(request):
    return render(request, 'djangogramm/index.html')


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


@login_required(login_url='login')
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = request.user
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()

    return render(request, 'djangogramm/create_post.html', {'form': form})


def post_list(request):
    posts = Post.objects.all()
    return render(request, 'djangogramm/post_list.html', {'posts': posts})
