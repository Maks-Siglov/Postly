from django.contrib.auth.views import LoginView
from django.urls import path

from djangogramm import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.registration, name='register'),
    path('profile/<str:link_key>/', views.profile, name='profile'),
    path('create_post/', views.create_post, name='create_post'),
    path('post_list/', views.post_list, name='post_list'),
    path(
        'login/',
        LoginView.as_view(template_name='djangogramm/login.html'),
        name='login')
]
