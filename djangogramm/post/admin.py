from django.contrib import admin

from post.models import Post, Tag


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    model = Post
    list_display = ("title", "owner", "creation_date")
    readonly_fields = ("creation_date",)
    search_fields = ("title", "owner", "content", "creation_date")
    list_filter = ("creation_date", "owner", "title")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    model = Tag
    list_display = ("name",)
    search_fields = ("name",)
    list_filter = ("name",)
