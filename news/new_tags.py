from django import template


from django.db.models import Count
from django.template.defaulttags import register

from news.models import New


@register.simple_tag
def get_most_commented_posts(count=5):
    return New.objects.annotate(
        total_comments=Count('reviews')
        ).order_by('-total_comments')[:count]
