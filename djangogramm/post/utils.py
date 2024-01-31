from django.db.models import QuerySet, Q

from post.models import Post


def q_search(query) -> QuerySet[Post] | None:
    if query.isdigit():
        return Post.objects.filter(id=int(query))

    search_fields = ("title__icontains", "content__icontains", "owner__username__icontains", "tags__name__icontains")
    query_filters = Q(**{field: query for field in search_fields})

    result = Post.objects.filter(query_filters).distinct()

    return result
