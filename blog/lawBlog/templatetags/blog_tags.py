
from ..models import Post,Category,Tag
from django import template
from django.db.models.aggregates import Count

# def get_recent_posts(num=5):
#     return Post.objects.all().order_by('-created_time')[:num]


# 为了能够通过 {% get_recent_posts %} 的语法在模板中调用这个函数，必须按照 Django 的规定注册这个函数为模板标签
register = template.Library()
# 最新文章模板标签
@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all().order_by('-created_time')[:num]

# 归档模板标签
@register.simple_tag
def archives():
    return Post.objects.dates('created_time', 'month', order='DESC')


# 分类模板标签
"""
def get_categories():
    # 别忘了在顶部引入 Category 类
    return Category.objects.all()
"""
@register.simple_tag
def get_categories():

    # 记得在顶部引入 count 函数
    # Count 计算分类下的文章数，其接受的参数为需要计数的模型的名称
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)


@register.simple_tag
def get_tags():
    # 记得在顶部引入 Tag model
    return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
