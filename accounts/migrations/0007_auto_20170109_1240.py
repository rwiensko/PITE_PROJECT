# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-09 12:40
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20170109_1238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='key_expires',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 11, 12, 40, 3, 45105)),
        ),
    ]