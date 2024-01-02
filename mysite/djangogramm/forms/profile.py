from django import forms

from djangogramm.models import UserProfile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["full_name", "bio", "avatar"]
