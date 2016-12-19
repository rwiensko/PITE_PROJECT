from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import login
from accounts.views import *

urlpatterns = [
    url(r'^register/$', 'register'),
    url(r'^activate/(?P<key>.+)$', 'activation'),
    url(r'^new-activation-link/(?P<user_id>\d+)/$', 'new_activation_link'),
]
