from allauth.socialaccount.models import SocialApp
from django.contrib import admin


class SocialAppAdmin(admin.ModelAdmin):
    model = SocialApp
    menu_icon = 'placeholder'
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('name', 'provider')


class SocialAdminGroup(admin.ModelAdmin):
    menu_label = 'Social_Account'
    menu_icon = 'users'
    menu_order = 10
    items = (SocialAppAdmin, )
