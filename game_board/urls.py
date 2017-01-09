from django.conf.urls import url
from . import views

app_name = 'game_board'

urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'^new/$', views.new_room, name='new_room'),
        url(r'^(?P<label>[\w-]{,50})/$', views.game_room, name='game_room'),
]
