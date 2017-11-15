
from django.conf.urls import url
from . import views

app_name = 'lawBlog'
urlpatterns = [
    url(r'^$',views.Index,name='index'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(), name='detail'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.ArchiveView.as_view(), name='archives'),
    url(r'^category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name='category'),
    url(r'full-width$', views.full_width, name='full-width'),
    url(r'^about$', views.about, name='about'),
    url(r'^contact$', views.contact, name='contact'),
    url(r'^blog$', views.BlogView.as_view(), name='blog'),
    url(r'^tag/(?P<pk>[0-9]+)/$', views.TagView.as_view(), name='tag'),

    # 其他 url 配置
    url(r'^search/$', views.search, name='search'),
]