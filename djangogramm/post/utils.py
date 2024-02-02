from django.db.models import QuerySet

from post.models import Post


def q_search(query) -> QuerySet[Post] | None:
    if query.isdigit():
        return Post.objects.filter(id=int(query))

    posts = (
            Post.objects.filter(title__iexact=query) |
            Post.objects.filter(owner__username__iexact=query) |
            Post.objects.filter(content__iexact=query) |
            Post.objects.filter(tags__name__iexact=query)
    ).select_related("owner")

    return posts
