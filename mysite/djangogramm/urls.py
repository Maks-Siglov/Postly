from django.urls import path

from djangogramm import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.registration, name='register'),
    path('profile/<str:link_key>/', views.profile, name='profile'),
]
