from django.conf.urls import url

from . import views

app_name = 'Contacts'
urlpatterns = [ url(r'^post', views.post_contact, name='post_contact'), ]