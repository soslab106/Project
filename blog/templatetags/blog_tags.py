from django import template
from ..models import Blog
from ..forms import BlogForm
from ..views import get_blog_list_common_data
register = template.Library()

@register.simple_tag
def get_blog_form():
    form = BlogForm()
    return form

@register.simple_tag
def get_user_blog_list(user):
    return Blog.objects.filter(author=user).order_by('-created_time')

@register.simple_tag
def get_user_blog_count(user):
    return Blog.objects.filter(author=user).count()