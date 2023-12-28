from django import forms
from django.contrib.auth.models import User


class RegistrationForm(forms.Form):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email']
