from django.db import models


class Post(models.Model):
    id = models.AutoField(primary_key=True)

    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='post_image/', blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    owner = models.ForeignKey(
        'djangogramm.User',
        on_delete=models.CASCADE,
        related_name='posts'
    )

    tag = models.ForeignKey(
        'djangogramm.Tag',
        on_delete=models.CASCADE,
        related_name='posts',
        blank=True,
        null=True
    )

    likes = models.ManyToManyField(
        'djangogramm.User',
        related_name='liked_post',
    )

    dislikes = models.ManyToManyField(
        'djangogramm.User',
        related_name='disliked_post',
    )

    def __str__(self):
        return self.title
