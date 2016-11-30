from django.conf.urls import url
from . import views

app_name = 'game_board'

urlpatterns = [
        url(r'^$', views.index, name='index'),
]
