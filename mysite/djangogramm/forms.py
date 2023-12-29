from django import forms
from django.contrib.auth.models import User

from djangogramm.models import UserProfile


class RegistrationForm(forms.Form):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['full_name', 'bio', 'avatar']
