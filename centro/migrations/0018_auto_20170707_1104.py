# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-07-07 16:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('centro', '0017_auto_20170707_1102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='knowledge',
            name='center',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='centro.Center', unique=True),
        ),
    ]
