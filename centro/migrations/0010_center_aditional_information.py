# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-11 19:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('centro', '0009_center_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='center',
            name='aditional_information',
            field=models.TextField(blank=True),
        ),
    ]
