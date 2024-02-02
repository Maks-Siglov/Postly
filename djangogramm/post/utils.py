from django.db.models import QuerySet

from post.models import Post


def q_search(query) -> QuerySet[Post] | None:
    if query.isdigit():
        return Post.objects.filter(id=int(query))

    posts = (
        Post.objects.filter(title__icontains=query) |
        Post.objects.filter(content__icontains=query) |
        Post.objects.filter(owner__username__icontains=query) |
        Post.objects.filter(tags__name__icontains=query)
    ).select_related("owner")

    return posts
