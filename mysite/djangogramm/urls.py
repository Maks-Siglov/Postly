from django.urls import path

from djangogramm.views import auth, main_page, post, profile

urlpatterns = [
    path('', main_page.index, name='index'),
    path('register/', auth.registration, name='register'),
    path(
        'profile_registration/<str:link_key>/',
        profile.profile_registration,
        name='profile_registration'
    ),
    path('profile/<username>', profile.profile, name='profile'),
    path('profile/<username>/edit', profile.edit_profile, name='edit_profile'),
    path('create_post/', post.create_post, name='create_post'),
    path('post_list/', post.post_list, name='post_list'),
    path('login/', auth.login_view, name='login'),
]
