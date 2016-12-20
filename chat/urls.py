from django.conf.urls import include, url
from chat import views

app_name = 'chat'

urlpatterns = [
    url(r'^$',  views.about, name='about'),
    url(r'^new/$', views.new_room, name='new_room'),
    url(r'^(?P<label>[\w-]{,50})/$', views.chat_room, name='chat_room'),
]
