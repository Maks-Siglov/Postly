from django import forms

from users.models import User


class EmailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email",)
