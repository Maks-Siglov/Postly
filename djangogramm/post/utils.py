from django.db.models import QuerySet, Q

from post.models import Post


def get_posts_q_search(value: str | None) -> QuerySet[Post]:
    if value is None:
        return Post.objects.select_related("owner")

    if value.isdigit():
        return Post.objects.filter(id=int(value)).select_related('owner')

    post_where = (
        Q(title__icontains=value) |
        Q(description__icontains=value) |
        Q(owner__username__icontains=value) |
        Q(tags__name__icontains=value)
    )

    return Post.objects.filter(post_where).select_related('owner')
