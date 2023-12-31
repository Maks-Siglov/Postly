from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse

from djangogramm.bl.email_generator import send_confirmation_email
from djangogramm.forms import RegistrationForm, ProfileForm, PostForm
from djangogramm.models import UserProfile, User, Post


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
