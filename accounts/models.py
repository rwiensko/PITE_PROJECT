from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models


class Friends(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    list_of_friends = ArrayField(models.IntegerField())

