from django.shortcuts import render
from django.http import HttpResponse

from django.shortcuts import render, get_object_or_404
from .models import Post
from comments.forms import CommentForm

# def index(request):
#     return HttpResponse("欢迎访问我的博客首页！")


# def index(request):
#     return render(request, 'lawBlog/index.html', context={
#                       'title': '我的博客首页',
#                       'welcome': '欢迎访问我的博客首页'
#                   })


import markdown
from .models import Post,Category
def index(request):
    post_list = Post.objects.all().order_by('-created_time')
    return render(request, 'lawBlog/index.html', context={'post_list': post_list})



# def detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     return render(request, 'lawBlog/detail.html', context={'post': post})


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # 记得在顶部引入 markdown 模块 需要在heml中加入 safe 标签
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                     'markdown.extensions.extra',
                                     'markdown.extensions.codehilite',
                                     'markdown.extensions.toc',
                                  ])
    return render(request, 'lawBlog/detail.html', context={'post': post})

# 归档
def archives(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    ).order_by('-created_time')
    return render(request, 'lawBlog/index.html', context={'post_list': post_list})

# Category
def category(request, pk):
    # 记得在开始部分导入 Category 类
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    return render(request, 'lawBlog/index.html', context={'post_list': post_list})


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])
    # 记得在顶部导入  SomtForm
    form = CommentForm()
    # 获取这篇 post 下的全部评论
    comment_list = post.comment_set.all()

    # 将文章、表单、以及文章下的评论列表作为模板变量传给 detail.html 模板，以便渲染相应数据。
    context = {'post': post,
               'SomtForm': form,
               'comment_list': comment_list,
               }
    return render(request, 'lawBlog/detail.html', context=context)