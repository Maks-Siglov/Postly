from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render

from post.utils import q_search
from users.models import User
from post.forms import CommentForm, PostForm
from post.models import Comment, Image, Post, Tag, Like


@login_required(login_url="users:login")
def create_post(request) -> HttpResponse:
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = request.user
            post.save()

            images = request.FILES.getlist("images")
            if images:
                for image in images:
                    Image.objects.create(image=image, post=post)

            tag_names = form.cleaned_data["tags"].split(",")
            for tag_name in tag_names:
                tag_name = tag_name.strip()
                if tag_name:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    post.tags.add(tag)

            return redirect("post:post_list")
    else:
        form = PostForm()

    return render(request, "post/create_post.html", {"form": form})


def post_list(request) -> HttpResponse:
    page = request.GET.get("page", 1)
    query = request.GET.get("q", None)
    order_by = request.GET.get("order_by", None)
    if query:
        posts = q_search(query)
    else:
        posts = Post.objects.all()

    if order_by:
        if order_by and order_by != "default" and order_by != 'likes':
            posts = posts.order_by(order_by)
        elif order_by == 'likes':
            posts = (
                Post.objects.annotate(like_count=Count('likes'))
                .order_by('-like_count')
            )

    paginator = Paginator(posts, 5)
    current_page = paginator.page(int(page))

    return render(request, "post/post_list.html", {"posts": current_page})


def user_posts(request, username: str) -> HttpResponse:
    page = request.GET.get("page", 1)
    query = request.GET.get("q", None)
    user = User.objects.get(username=username)
    order_by = request.GET.get("order_by", None)
    if query:
        posts = q_search(query)
    else:
        posts = Post.objects.filter(owner=user)

    if order_by:
        if order_by and order_by != "default" and order_by != 'likes':
            posts = posts.order_by(order_by)
        elif order_by == 'likes':
            posts = (
                Post.objects.annotate(like_count=Count('likes'))
                .order_by('-like_count')
            )

    paginator = Paginator(posts, 5)
    current_page = paginator.page(int(page))

    if request.user == user:
        return render(request, "post/user_posts.html", {"posts": current_page})

    return render(request, "post/post_list.html", {"posts": posts})


@login_required(login_url="users:login")
def post_detail(request, post_id: int) -> HttpResponse:
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post)
    comment_form = CommentForm()

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.owner = request.user
            comment.save()

    return render(
        request,
        "post/post_detail.html",
        {
            "post": post,
            "Post": Post,
            "Comment": Comment,
            "comments": comments,
            "comment_form": comment_form,
        },
    )


@login_required(login_url="users:login")
def edit_post(request, post_id: int) -> HttpResponseRedirect:
    post = Post.objects.get(id=post_id)
    if request.user != post.owner:
        messages.error(
            request, "You do not have permission to view this userprofile."
        )
        return redirect("post:post_list")

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():

            tag_names = form.cleaned_data["tags"].split(",")
            for tag_name in tag_names:
                tag_name = tag_name.strip()
                if tag_name:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    post.tags.add(tag)

            images = request.FILES.getlist("images")
            if images:
                recent_images = Image.objects.filter(post=post)
                recent_images.delete()
                for image in images:
                    Image.objects.create(image=image, post=post)

            form.save()
            messages.success(request, "Post updated successfully.")
            return redirect("post:user_posts", post.owner.username)
    else:
        form = PostForm(instance=post)

    return render(
        request,
        "post/edit_post.html",
        {"form": form},
    )


@login_required(login_url="users:login")
def delete_post(request, post_id: int) -> HttpResponse | HttpResponseRedirect:
    post = get_object_or_404(Post, id=post_id)

    if request.user != post.owner:
        messages.error(
            request, "You do not have permission to view this userprofile."
        )
        return redirect("post:post_list")

    if request.method == "POST":
        post.delete()
        return redirect("post:user_posts", post.owner.username)

    return render(
        request,
        "post/delete_post.html",
        {"post": post, "user": post.owner},
    )


@login_required(login_url="users:login")
def like_post(request, post_id: int) -> HttpResponseRedirect:
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    like_content_type = ContentType.objects.get_for_model(Post)

    dislike = Like.objects.filter(
        value=False,
        owner=user,
        content_type=like_content_type,
        object_id=post.id,
    ).first()
    if dislike:
        dislike.delete()

    like, created = Like.objects.get_or_create(
        value=True,
        owner=user,
        content_type=like_content_type,
        object_id=post.id,
    )
    if created:
        like.save()
    else:
        like.delete()

    return redirect("post:post_detail", post.id)


@login_required(login_url="users:login")
def dislike_post(request, post_id: int) -> HttpResponseRedirect:
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    like_content_type = ContentType.objects.get_for_model(Post)

    like = Like.objects.filter(
        value=True,
        owner=user,
        content_type=like_content_type,
        object_id=post.id,
    ).first()
    if like:
        like.delete()

    dislike, created = Like.objects.get_or_create(
        value=False,
        owner=user,
        content_type=like_content_type,
        object_id=post.id,
    )
    if created:
        dislike.save()
    else:
        dislike.delete()

    return redirect("post:post_detail", post.id)


@login_required(login_url="users:login")
def like_comment(request, comment_id: int) -> HttpResponseRedirect:
    comment = get_object_or_404(Comment, id=comment_id)
    user = request.user

    like_content_type = ContentType.objects.get_for_model(Comment)

    dislike = Like.objects.filter(
        value=False,
        owner=user,
        content_type=like_content_type,
        object_id=comment.id,
    ).first()
    if dislike:
        dislike.delete()

    like, created = Like.objects.get_or_create(
        value=True,
        owner=user,
        content_type=like_content_type,
        object_id=comment.id,
    )
    if created:
        like.save()
    else:
        like.delete()

    return redirect("post:post_detail", comment.post.id)


@login_required(login_url="users:login")
def dislike_comment(request, comment_id: int) -> HttpResponseRedirect:
    comment = get_object_or_404(Comment, id=comment_id)
    user = request.user

    like_content_type = ContentType.objects.get_for_model(Comment)

    like = Like.objects.filter(
        value=True,
        owner=user,
        content_type=like_content_type,
        object_id=comment.id,
    ).first()
    if like:
        like.delete()

    dislike, created = Like.objects.get_or_create(
        value=False,
        owner=user,
        content_type=like_content_type,
        object_id=comment.id,
    )
    if created:
        dislike.save()
    else:
        dislike.delete()

    return redirect("post:post_detail", comment.post.id)
