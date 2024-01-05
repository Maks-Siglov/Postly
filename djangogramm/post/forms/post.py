from django import forms

from post.models import Post


class PostForm(forms.ModelForm):
    tags = forms.CharField(max_length=255, required=False)
    image = forms.ImageField(required=False)

    class Meta:
        model = Post
        fields = ["title", "content"]
