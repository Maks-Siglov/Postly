from django.contrib import admin

from djangogramm.models import Comment, Post, Tag, User, UserProfile

admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Tag)
