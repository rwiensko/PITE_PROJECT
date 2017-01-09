from django.db import models


class Player(models.Model):
    id = models.AutoField(primary_key=True)
    label = models.CharField(max_length=50)
