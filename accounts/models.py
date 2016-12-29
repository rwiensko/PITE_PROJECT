from __future__ import unicode_literals
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    activation_key = models.CharField(max_length=40, default=000)
    key_expires = models.DateTimeField(default=datetime.today() + timedelta(days=2) )
    list_of_friends = ArrayField(models.IntegerField(), default=[])

    def add_friend(self, friend_id):
        self.list_of_friends.append(friend_id)

    def __unicode__(self):
        return unicode(self.user.id) + unicode(self.list_of_friends)

