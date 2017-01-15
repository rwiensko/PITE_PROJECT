from django.db import models
from django.contrib.auth.models import User


class Player(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    label = models.CharField(max_length=50)
