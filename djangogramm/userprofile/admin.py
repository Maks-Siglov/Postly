from django.contrib import admin

from userprofile.models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    model = UserProfile
    list_display = ("full_name",)
    search_fields = ("full_name",)
    list_filter = ("full_name",)
