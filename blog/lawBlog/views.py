from django.shortcuts import render
from django.http import HttpResponse

from django.shortcuts import render, get_object_or_404
from .models import Post ,Tag
from Contacts.forms import ContactForm
from comments.forms import CommentForm

from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.db.models import Q
# def index(request):
#     return HttpResponse("欢迎访问我的博客首页！")


# def index(request):
#     return render(request, 'lawBlog/index.html', context={
#                       'title': '我的博客首页',
#                       'welcome': '欢迎访问我的博客首页'
#                   })


def full_width(request):
    return render(request, 'lawBlog/blog.html')

def contact(request):
    form = ContactForm()
    context = {'contactForm': form}
    return render(request, 'lawBlog/contact.html',context=context)

def about(request):
    return render(request, 'lawBlog/about.html')


def Index(request):
    return render(request, 'lawBlog/index.html')

import markdown
from .models import Post,Category

"""
def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'lawBlog/detail.html', context={'post': post})

"""


"""
def index(request):
    post_list = Post.objects.all().order_by('-created_time')
    return render(request, 'lawBlog/index.html', context={'post_list': post_list})
"""
from django.views.generic import ListView
# 将 index 视图函数改写为类视图
class BlogView(ListView):
    model = Post
    template_name = 'lawBlog/blog.html'
    context_object_name = 'post_list'

    # 指定 paginate_by 属性后开启分页功能,其值代表每一页包含的文章数量
    paginate_by = 1

# 归档
"""
def archives(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    ).order_by('-created_time')
    return render(request, 'lawBlog/index.html', context={'post_list': post_list})
"""
class ArchiveView(BlogView):
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchiveView,self).get_queryset().filter(created_time__year=year,
                                                             created_time__month=month
                                                             ).order_by('-created_time')

# Category

"""
def category(request, pk):
    # 记得在开始部分导入 Category 类
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    return render(request, 'lawBlog/index.html', context={'post_list': post_list})
"""

class CategoryView(ListView):
    model = Post
    template_name = 'lawBlog/blog.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        cate = get_object_or_404(Category,pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)

"""
def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])
    # 阅读量 +1
    post.increase_views()
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
"""

from django.views.generic import DetailView

class PostDetailView(DetailView):
    model = Post
    template_name = 'lawBlog/detail.html'
    context_object_name = 'post'

    def get(self,request,*args,**kwargs):
        # 覆写 get 方法的目的是因为每当文章被访问一次，就得将文章阅读量 +1
        # get 方法返回的是一个 HttpResponse 实例
        # 之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后
        # 才有 self.object 属性，其值为 Post 模型实例，即被访问的文章 post
        response = super(PostDetailView, self).get(request, *args, **kwargs)

        # 将文章阅读量 +1
        # 注意 self.object 的值就是被访问的文章 post
        self.object.increase_views()

        # 视图必须返回一个 HttpResponse 对象
        return response

    def get_object(self, queryset=None):

        # 覆写 get_object 方法的目的是因为需要对 post 的 body 值进行渲染

        md = markdown.Markdown(extensions=[
                                   'markdown.extensions.extra',
                                   'markdown.extensions.codehilite',
                                   'markdown.extensions.toc',
                                    # 记得在顶部引入 TocExtension 和 slugify
                                    TocExtension(slugify=slugify),
                               ])
        post = super(PostDetailView,self).get_object(queryset=None)
        post.body = md.convert(post.body)
        post.toc = md.toc
        """
        post.body = markdown.markdown(post.body,
                                      extensions=[
                                          'markdown.extensions.extra',
                                          'markdown.extensions.codehilite',
                                          'markdown.extensions.toc',
                                      ])
        """

        return post


    def get_context_data(self, **kwargs):
        # 覆写 get_context_data 的目的是因为除了将 post 传递给模板外（DetailView 已经帮我们完成），
        # 还要把评论表单、post 下的评论列表传递给模板。

        context = super(PostDetailView,self).get_context_data(**kwargs)
        form = CommentForm()
        commen_list = self.object.comment_set.all()
        context.update({
            'form':form,
            'comment_list':commen_list
        })

        return context




class TagView(ListView):
    model = Post
    template_name = 'lawBlog/blog.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        tag = get_object_or_404(Tag,pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)



def search(request):
    q = request.GET.get('q')
    error_msg = ''
    if not q:
        error_msg = "请输入关键词"
        return render(request, 'lawBlog/blog.html', {'error_msg': error_msg})

    post_list = Post.objects.filter(Q(title__contains=q)|Q(body__contains=q))
    return  render(request,'lawBlog/blog.html',
                   {'error_msg': error_msg,
                    'post_list': post_list}
                   )






