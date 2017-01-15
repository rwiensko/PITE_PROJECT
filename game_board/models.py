from django.db import models

from accounts.models import Profile


class Player(models.Model):
    id = models.AutoField(primary_key=True)
    label = models.CharField(max_length=50)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
