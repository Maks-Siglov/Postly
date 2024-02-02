from django.contrib import admin

from post.models import Post, Comment
from users.models import User


class PostInline(admin.TabularInline):
    model = Post


class CommentInline(admin.TabularInline):
    model = Comment


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ("username", "email")
    search_fields = ("username", "email")
    list_filter = ("username", "email")
    inlines = (PostInline, CommentInline)
