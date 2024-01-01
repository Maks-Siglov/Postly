from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from djangogramm.forms import PostForm
from djangogramm.models import Post, Tag


@login_required(login_url='login')
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = request.user

            tag_name = form.cleaned_data['tag']
            if tag_name:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                post.tag = tag

            post.save()
            return redirect('post_list')
    else:
        form = PostForm()

    return render(request, 'djangogramm/post/create_post.html', {'form': form})


def post_list(request):
    posts = Post.objects.all()
    return render(request, 'djangogramm/post/post_list.html', {'posts': posts})


@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    if user in post.likes.all():
        post.likes.remove(user)
    else:
        post.likes.add(user)

    return redirect('post_list')
