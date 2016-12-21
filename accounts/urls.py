from django.conf.urls import url
from accounts.views import *

urlpatterns = [
    url(r'^$', add_nothing),
    url(r'^added_friend/(?P<user_id>\d+)/$', add_friend)
]
