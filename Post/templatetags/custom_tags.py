from atexit import register
from django import template
from Post.models import Post, Category, Tag
from django.db.models import Q

register = template.Library()

@register.simple_tag(name="featured_posts")
def all_featured_posts():
    return Post.objects.filter(Q(published=True) & Q(featured=True))

@register.simple_tag(name="categories")
def all_categories():
    return Category.objects.all()
    
@register.simple_tag(name="tags")
def all_tags():
    return Tag.objects.all()