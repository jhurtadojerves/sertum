# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-07-25 01:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('centro', '0021_auto_20170724_1135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='center',
            name='aditional_information',
            field=models.TextField(blank=True, verbose_name='Place Description'),
        ),
    ]
