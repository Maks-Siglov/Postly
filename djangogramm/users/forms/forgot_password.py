from django import forms
from django.contrib.auth.forms import PasswordResetForm

from users.models import User


class UserForgotPasswordForm(PasswordResetForm):
    email = forms.EmailField(required=True, max_length=254)

    class Meta:
        model = User
        fields = ("email",)
