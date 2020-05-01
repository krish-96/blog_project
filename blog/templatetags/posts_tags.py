from blog.models import Post, Author, Comment
from django.contrib.auth.models import User
from django import template
from django.db.models import Q
register = template.Library()

@register.simple_tag(name='total_posts')
def total_posts():
    return Post.objects.all().count()

@register.simple_tag(name='total_public_posts')
def total_public_posts():
    return Post.objects.all().filter(~Q(status='D'),~Q(privacy='Private')).count()

@register.simple_tag(name='total_no_authors')
def all_authors():
    return Author.objects.all().count()

@register.simple_tag(name='total_no_users')
def all_users():
    return User.objects.all().count()


@register.simple_tag(name='total_private_posts')
def total_private_posts():
    return Post.objects.all().filter(Q(status='D')|Q(privacy='Private')).count()

# @register.simple_tag(name='total_private_posts')
# def total_private_posts():
#     return Post.objects.filter(privacy='private').count()


