from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from post.models import Comment, Dislike, Like, Post, Tag


class LikeInline(GenericTabularInline):
    model = Like


class DislikeInline(GenericTabularInline):
    model = Dislike


class CommentInline(admin.TabularInline):
    model = Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    model = Post
    list_display = ("title", "owner", "creation_date")
    readonly_fields = ("creation_date",)
    search_fields = ("title", "owner__username", "content", "creation_date")
    list_filter = ("creation_date", "owner", "title")
    inlines = (CommentInline, LikeInline, DislikeInline)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    model = Tag
    list_display = ("name",)
    search_fields = ("name",)
    list_filter = ("name",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ("post", "owner", "creation_date")
    list_filter = ("creation_date", "owner", "post")
    search_fields = ("owner", "post", "content")
    readonly_fields = ("creation_date",)
    inlines = (LikeInline, DislikeInline)
