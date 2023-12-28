from django.urls import path

from djangogramm import views

urlpatterns = [
    path('register/', views.registration, name='registration'),
]
