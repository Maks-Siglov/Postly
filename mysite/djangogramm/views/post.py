from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from djangogramm.forms import PostForm, CommentForm
from djangogramm.models import Post, Tag, Comment


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


def post_detail(request, post_id: int):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post)
    comment_form = CommentForm()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.owner = request.user
            comment.save()

    return render(
        request,
        'djangogramm/post/post_detail.html',
        {'post': post, 'comments': comments, 'comment_form': comment_form}
    )


@login_required(login_url='login')
def like_post(request, post_id: int):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    if user in post.likes.all():
        post.likes.remove(user)
    else:
        post.likes.add(user)

        if user in post.dislikes.all():
            post.dislikes.remove(user)

    return redirect('post_list')


@login_required(login_url='login')
def dislike_post(request, post_id: int):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    if user in post.dislikes.all():
        post.dislikes.remove(user)
    else:
        post.dislikes.add(user)

        if user in post.likes.all():
            post.likes.remove(user)

    return redirect('post_list')
