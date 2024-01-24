from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render

from post.forms import CommentForm, PostForm
from post.models import Comment, Image, Post, Tag
from post.selectors import (
    get_posts,
    get_users_post,
    get_following_posts,
    get_like,
    get_dislike,
)
from users.models import User


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
    posts = get_posts(query, order_by)

    paginator = Paginator(posts, 5)
    current_page = paginator.page(int(page))

    return render(request, "post/post_list.html", {"posts": current_page})


def user_posts(request, username: str) -> HttpResponse:
    page = request.GET.get("page", 1)
    query = request.GET.get("q", None)
    order_by = request.GET.get("order_by", None)
    user = User.objects.get(username=username)
    posts = get_users_post(user, query, order_by)

    paginator = Paginator(posts, 5)
    current_page = paginator.page(int(page))

    if request.user == user:
        return render(
            request,
            "post/my_posts.html",
            {"posts": current_page, "user": user}
        )

    return render(
        request,
        "post/user_posts.html",
        {"posts": current_page, "user": user}
    )


@login_required(login_url="users:login")
def following_posts(request, username: str) -> HttpResponse:
    page = request.GET.get("page", 1)
    query = request.GET.get("q", None)
    order_by = request.GET.get("order_by", None)
    user = User.objects.get(username=username)

    posts = get_following_posts(user, query, order_by)

    paginator = Paginator(posts, 5)
    current_page = paginator.page(int(page))

    return render(request, "post/following_feed.html", {"posts": current_page})


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
            return redirect("post:post_detail", post_id=post_id)

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
def edit_post(request, post_id: int) -> HttpResponse | HttpResponseRedirect:
    post = Post.objects.get(id=post_id)
    if request.user != post.owner:
        messages.error(
            request, "You do not have permission to do this."
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
            request, "You do not have permission to do this."
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

    dislike, like, like_created = get_like(post, user)

    if dislike:
        dislike.delete()

    if like_created:
        like.save()
    else:
        like.delete()

    return redirect("post:post_detail", post.id)


@login_required(login_url="users:login")
def dislike_post(request, post_id: int) -> HttpResponseRedirect:
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    like, dislike, dislike_created = get_dislike(post, user)

    if like:
        like.delete()

    if dislike_created:
        dislike.save()
    else:
        dislike.delete()

    return redirect("post:post_detail", post.id)


@login_required(login_url="users:login")
def edit_comment(
        request, comment_id: int
) -> HttpResponse | HttpResponseRedirect:
    comment = Comment.objects.get(id=comment_id)

    if request.user != comment.owner:
        messages.error(
            request, "You do not have permission to do this."
        )
        return redirect("post:post_list")

    if request.method == "POST":
        form = CommentForm(instance=comment, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('post:post_detail', comment.post.id)

    else:
        form = CommentForm(instance=comment)

    return render(request, "post/edit_comment.html", {"form": form})


@login_required(login_url="users:login")
def delete_comment(request, comment_id: int) -> HttpResponseRedirect:
    comment = Comment.objects.get(id=comment_id)

    if request.user != comment.owner:
        messages.error(
            request, "You do not have permission to do this."
        )
        return redirect("post:post_list")

    comment.delete()
    return redirect('post:post_detail', comment.post.id)


@login_required(login_url="users:login")
def like_comment(request, comment_id: int) -> HttpResponseRedirect:
    comment = get_object_or_404(Comment, id=comment_id)
    user = request.user

    dislike, like, like_created = get_like(comment, user)

    if dislike:
        dislike.delete()

    if like_created:
        like.save()
    else:
        like.delete()

    return redirect("post:post_detail", comment.post.id)


@login_required(login_url="users:login")
def dislike_comment(request, comment_id: int) -> HttpResponseRedirect:
    comment = get_object_or_404(Comment, id=comment_id)
    user = request.user

    like, dislike, dislike_created = get_dislike(comment, user)

    if like:
        like.delete()

    if dislike_created:
        dislike.save()
    else:
        dislike.delete()

    return redirect("post:post_detail", comment.post.id)
