from django.contrib.auth.views import LoginView
from django.urls import path

from djangogramm.views import auth, main_page, post, profile

urlpatterns = [
    path('', main_page.index, name='index'),
    path('register/', auth.registration, name='register'),
    path('profile/<str:link_key>/', profile.profile, name='profile'),
    path('create_post/', post.create_post, name='create_post'),
    path('post_list/', post.post_list, name='post_list'),
    path(
        'login/',
        LoginView.as_view(template_name='djangogramm/login.html'),
        name='login'
    ),
]
