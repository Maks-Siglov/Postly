from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import redirect, render

from post.forms import CommentForm, PostForm
from post.models import Comment, Image, Post, Tag
from post.selectors import (
    get_dislike,
    get_following_posts,
    get_like,
    get_post_by_id,
    get_post_comments,
    get_posts,
    get_user_posts,
)

from users.models import User


@login_required(login_url="users:login")
def create_post(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
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
                    tag, _ = Tag.objects.get_or_create(name=tag_name)
                    post.tags.add(tag)

            return redirect("post:post_list")
    else:
        form = PostForm()

    return render(request, "post/create_post.html", {"form": form})


def post_list(request: HttpRequest) -> HttpResponse:
    page = request.GET.get("page", settings.DEFAULT_PAGE)
    search_value = request.GET.get("search", None)
    order_by = request.GET.get("order_by", None)
    posts = get_posts(search_value, order_by)

    paginator = Paginator(posts, settings.POSTS_PER_PAGE)
    current_page = paginator.page(int(page))

    return render(request, "post/post_list.html", {"posts": current_page})


def user_posts(request: HttpRequest, username: str) -> HttpResponse:
    page = request.GET.get("page", settings.DEFAULT_PAGE)
    search_value = request.GET.get("search", None)
    order_by = request.GET.get("order_by", None)
    user = User.objects.get(username=username)
    posts = get_user_posts(user, search_value, order_by)

    paginator = Paginator(posts, settings.POSTS_PER_PAGE)
    current_page = paginator.page(int(page))

    if request.user == user:
        return render(
            request,
            "post/my_posts.html",
            {"posts": current_page, "user": user},
        )

    return render(
        request, "post/user_posts.html", {"posts": current_page, "user": user}
    )


@login_required(login_url="users:login")
def following_posts(request: HttpRequest, username: str) -> HttpResponse:
    page = request.GET.get("page", settings.DEFAULT_PAGE)
    search_value = request.GET.get("search", None)
    order_by = request.GET.get("order_by", None)
    user = User.objects.get(username=username)

    posts = get_following_posts(user, search_value, order_by)

    paginator = Paginator(posts, settings.POSTS_PER_PAGE)
    current_page = paginator.page(int(page))

    return render(request, "post/following_feed.html", {"posts": current_page})


@login_required(login_url="users:login")
def post_detail(
    request: HttpRequest, post_id: int
) -> HttpResponse | HttpResponseRedirect:
    try:
        post = get_post_by_id(post_id)
    except ObjectDoesNotExist:
        messages.error(request, f"Post {post_id} not exist")
        return redirect("post:post_list")

    comments = get_post_comments(post)
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
def edit_post(
    request: HttpRequest, post_id: int
) -> HttpResponse | HttpResponseRedirect:
    try:
        post = Post.objects.get(id=post_id)
    except ObjectDoesNotExist:
        messages.error(request, f"Post {post_id} not exist")
        return redirect("post:post_list")

    if request.user != post.owner:
        messages.error(request, "You do not have permission to do this.")
        return redirect("post:post_list")

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():

            tag_names = form.cleaned_data["tags"].split(",")
            for tag_name in tag_names:
                tag_name = tag_name.strip()
                if tag_name:
                    tag, _ = Tag.objects.get_or_create(name=tag_name)
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
        {
            "form": form,
            "post": post,
        },
    )


@login_required(login_url="users:login")
def delete_post(
    request: HttpRequest, post_id: int
) -> HttpResponse | HttpResponseRedirect:
    try:
        post = Post.objects.get(id=post_id)
    except ObjectDoesNotExist:
        messages.error(request, f"Post {post_id} not exist")
        return redirect("post:post_list")

    if request.user != post.owner:
        messages.error(request, "You do not have permission to do this.")
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
def like_post(
    request: HttpRequest, post_id: int
) -> JsonResponse | HttpResponseRedirect:
    try:
        post = Post.objects.get(id=post_id)
    except ObjectDoesNotExist:
        messages.error(request, f"Post {post_id} not exist")
        return redirect("post:post_list")

    dislike, like, like_created = get_like(post, request.user)

    if dislike:
        dislike.delete()

    if like_created:
        like.save()
    else:
        like.delete()

    return JsonResponse(
        {
            "success": True,
            "like_count": post.likes.count(),
            "dislike_count": post.dislikes.count(),
        }
    )


@login_required(login_url="users:login")
def dislike_post(
    request: HttpRequest, post_id: int
) -> JsonResponse | HttpResponseRedirect:
    try:
        post = Post.objects.get(id=post_id)
    except ObjectDoesNotExist:
        messages.error(request, f"Post {post_id} not exist")
        return redirect("post:post_list")

    like, dislike, dislike_created = get_dislike(post, request.user)

    if like:
        like.delete()

    if dislike_created:
        dislike.save()
    else:
        dislike.delete()

    return JsonResponse(
        {
            "success": True,
            "like_count": post.likes.count(),
            "dislike_count": post.dislikes.count(),
        }
    )


@login_required(login_url="users:login")
def edit_comment(
    request: HttpRequest, comment_id: int
) -> HttpResponse | HttpResponseRedirect:
    try:
        comment = Comment.objects.get(id=comment_id)
    except ObjectDoesNotExist:
        messages.error(request, f"Comment {comment_id} not exist")
        return redirect("post:post_list")

    if request.user != comment.owner:
        messages.error(request, "You do not have permission to do this.")
        return redirect("post:post_list")

    if request.method == "POST":
        form = CommentForm(instance=comment, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("post:post_detail", comment.post.id)

    else:
        form = CommentForm(instance=comment)

    return render(
        request, "post/edit_comment.html", {"form": form, "comment": comment}
    )


@login_required(login_url="users:login")
def delete_comment(
    request: HttpRequest, comment_id: int
) -> HttpResponseRedirect:
    try:
        comment = Comment.objects.get(id=comment_id)
    except ObjectDoesNotExist:
        messages.error(request, f"Comment {comment_id} not exist")
        return redirect("post:post_list")

    if request.user != comment.owner:
        messages.error(request, "You do not have permission to do this.")
        return redirect("post:post_list")

    comment.delete()
    return redirect("post:post_detail", comment.post.id)


@login_required(login_url="users:login")
def like_comment(
    request: HttpRequest, comment_id: int
) -> JsonResponse | HttpResponseRedirect:
    try:
        comment = Comment.objects.get(id=comment_id)
    except ObjectDoesNotExist:
        messages.error(request, f"Comment {comment_id} not exist")
        return redirect("post:post_list")

    dislike, like, like_created = get_like(comment, request.user)

    if dislike:
        dislike.delete()

    if like_created:
        like.save()
    else:
        like.delete()

    return JsonResponse(
        {
            "success": True,
            "like_count": comment.likes.count(),
            "dislike_count": comment.dislikes.count(),
        }
    )


@login_required(login_url="users:login")
def dislike_comment(
    request: HttpRequest, comment_id: int
) -> JsonResponse | HttpResponseRedirect:
    try:
        comment = Comment.objects.get(id=comment_id)
    except ObjectDoesNotExist:
        messages.error(request, f"Comment {comment_id} not exist")
        return redirect("post:post_list")

    like, dislike, dislike_created = get_dislike(comment, request.user)

    if like:
        like.delete()

    if dislike_created:
        dislike.save()
    else:
        dislike.delete()

    return JsonResponse(
        {
            "success": True,
            "like_count": comment.likes.count(),
            "dislike_count": comment.dislikes.count(),
        }
    )
