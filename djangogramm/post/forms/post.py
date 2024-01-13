from django import forms

from post.models import Post


class PostForm(forms.ModelForm):
    tags = forms.CharField(max_length=255, required=False)
    images = forms.FileField(
        required=False
    )

    class Meta:
        model = Post
        fields = ("title", "content")
