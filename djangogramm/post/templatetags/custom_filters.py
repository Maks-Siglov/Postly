from django import template
from django.utils.http import urlencode

from post.models import Like

register = template.Library()


@register.filter
def likes_count(content_model, object_id):
    return Like.objects.likes(content_model, object_id).count()


@register.filter
def dislikes_count(content_model, object_id):
    return Like.objects.dislikes(content_model, object_id).count()


@register.simple_tag(takes_context=True)
def change_params(context, **kwargs):
    query = context["request"].GET.dict()
    query.update(kwargs)
    return urlencode(query)
