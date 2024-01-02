from django import forms

from djangogramm.models import Post


class PostForm(forms.ModelForm):
    tag = forms.CharField(max_length=255, required=False)

    class Meta:
        model = Post
        fields = ["title", "content", "image"]
