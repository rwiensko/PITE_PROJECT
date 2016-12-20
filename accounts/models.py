from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    activation_key = models.CharField(max_length=40)
    key_expires = models.DateTimeField()
    list_of_friends = ArrayField(models.IntegerField(), default=[])

    def add_friend(self, friend_id):
        self.list_of_friends.append(friend_id)

