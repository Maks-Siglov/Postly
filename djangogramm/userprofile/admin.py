from django.contrib import admin

from userprofile.models import UserProfile, Follow


class FollowerInline(admin.TabularInline):
    model = Follow
    fk_name = 'following'


class FollowingInline(admin.TabularInline):
    model = Follow
    fk_name = 'follower'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    model = UserProfile
    list_display = ("full_name", "user")
    search_fields = ("full_name",)
    list_filter = ("full_name",)
    inlines = (FollowerInline, FollowingInline)
