from django.db.models import Q, QuerySet

from post.models import Post


def get_posts_q_search(value: str | None) -> QuerySet[Post]:
    if value is None:
        return (
            Post.objects
            .select_related("owner")
            .prefetch_related("likes", "dislikes", "tags")
        )

    if value.isdigit():
        return (
            Post.objects
            .filter(id=int(value))
            .select_related("owner")
            .prefetch_related("likes", "dislikes", "tags")
        )

    post_where = (
        Q(title__icontains=value)
        | Q(content__icontains=value)
        | Q(owner__username__icontains=value)
        | Q(tags__name__icontains=value)
    )

    return (
        Post.objects
        .filter(post_where)
        .select_related("owner")
        .prefetch_related("likes", "dislikes", "tags")
    )
