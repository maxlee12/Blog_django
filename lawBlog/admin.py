from django.contrib import admin
from .models import Post, Category, Tag
# Register your models here.

# admin post列表页面，我们只看到了文章的标题，但是我们希望它显示更加详细的信息，这需要我们来定制
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_time', 'modified_time', 'category', 'author']

admin.site.register(Post,PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)


