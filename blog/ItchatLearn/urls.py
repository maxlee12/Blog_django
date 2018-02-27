from django.conf.urls import url
from . import views

app_name = 'ItchatLearn'
urlpatterns = [
    url(r'^$',views.itchats,name='itchats'),
]
