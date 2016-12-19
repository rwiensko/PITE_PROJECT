"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import login
from accounts.views import *
from . import views

urlpatterns = [
    url(r'^$', login),
    url(r'^logout/$', logout_page),
    url(r'^accounts/login/$', login),  # If user is not login it will redirect to login page
    url(r'^register/$', register),
    url(r'^activate/(?P<key>.+)$', activation),
    url(r'^new-activation-link/(?P<user_id>\d+)/$', new_activation_link),
    url(r'^register/success/$', register_success),
    url(r'^home/$', home),
    url(r'^game-board/', include('game_board.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^new/$', views.new_room, name='new_room'),
    url(r'^(?P<label>[\w-]{,50})/$', views.chat_room, name='chat_room'),
]
