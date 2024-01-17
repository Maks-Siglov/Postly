from django.contrib.postgres.search import (
    SearchQuery,
    SearchVector,
    SearchRank,
)
from django.db.models import QuerySet

from post.models import Post


def q_search(query) -> QuerySet[Post] | None:
    if query.isdigit() and len(query) <= 5:
        return Post.objects.filter(id=int(query))

    vector = SearchVector("title", "content", "owner__username")
    query = SearchQuery(query)

    result = (
        Post.objects.annotate(rank=SearchRank(vector, query))
        .filter(rank__gt=0)
        .order_by("-rank")
    )

    return result
