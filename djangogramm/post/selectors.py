from django.contrib.contenttypes.models import ContentType
from django.db.models import Count, Model, QuerySet

from post.models import Comment, Dislike, Like, Post
from post.utils import get_posts_q_search

from users.models import User


def get_posts(value: str | None, order_by: str | None) -> QuerySet[Post]:

    posts = get_posts_q_search(value)

    if order_by and posts:
        posts = _order_by_post(posts, order_by)

    return posts


def get_user_posts(
    user: User, value: str | None, order_by: str | None
) -> QuerySet[Post]:

    posts = get_posts_q_search(value).filter(owner=user)

    if order_by and posts:
        _order_by_post(posts, order_by)

    return posts


def get_following_posts(
    user: User, value: str | None, order_by: str | None
) -> QuerySet[Post]:

    posts = get_posts_q_search(value)

    following_id_list = list(
        user.profile.following.all().values_list("following_id", flat=True)
    )

    posts = posts.filter(
        owner__in=User.objects.filter(id__in=following_id_list)
    )

    if order_by and posts:
        _order_by_post(posts, order_by)

    return posts


def _order_by_post(
    posts: QuerySet[Post], order_by: str | None
) -> QuerySet[Post]:
    if order_by is None:
        return posts

    if order_by == "likes":
        return (
            posts
            .annotate(like_count=Count("likes"))
            .order_by("-like_count")
        )

    return posts.order_by(order_by)


def get_post_by_id(post_id: int) -> Post | None:
    return (
        Post.objects.select_related("owner")
        .prefetch_related("likes", "dislikes", "tags")
        .get(id=post_id)
    )


def get_post_comments(post: Post) -> QuerySet[Comment]:
    return (
        Comment.objects.select_related("owner")
        .prefetch_related("likes", "dislikes")
        .filter(post=post)
    )


def get_like(instance: Model, user: User) -> tuple[Dislike | None, Like, bool]:
    content_type = ContentType.objects.get_for_model(instance.__class__)

    dislike = Dislike.objects.filter(
        owner=user,
        content_type=content_type,
        object_id=instance.id,
    ).first()

    like, like_created = Like.objects.get_or_create(
        owner=user,
        content_type=content_type,
        object_id=instance.id,
    )

    return dislike, like, like_created


def get_dislike(
    instance: Model, user: User
) -> tuple[Like | None, Dislike, bool]:
    content_type = ContentType.objects.get_for_model(instance.__class__)

    like = Like.objects.filter(
        owner=user,
        content_type=content_type,
        object_id=instance.id,
    ).first()

    dislike, dislike_created = Dislike.objects.get_or_create(
        owner=user,
        content_type=content_type,
        object_id=instance.id,
    )
    return like, dislike, dislike_created
