# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-09-12 00:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('centro', '0033_auto_20170911_1913'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicecenter',
            name='cost',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='servicecenter',
            name='observation',
            field=models.TextField(default=' '),
        ),
    ]
