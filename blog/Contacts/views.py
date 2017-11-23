from django.shortcuts import render

from .models import Contact
from  .forms import ContactForm

from django.core.mail import send_mail

# 发送邮件的说明
# https://code.ziqiangxuetang.com/django/django-send-email.html

# Create your views here.

def post_contact(request):

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():

            msg = form.save(commit=False)
            msg.save()

            send_mail(msg.subject, msg.email + "-----" +msg.message, '760822901@qq.com',
                      ['law@xqopen.cn'], fail_silently=False)

            return render(request, 'lawBlog/contact.html',context={'postReturn': '提交成功'})
        else:
            return render(request, 'lawBlog/index.html')