# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-10-21 13:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('centro', '0039_auto_20171021_0847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='knowledge',
            name='center',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='knowledge', to='centro.Center'),
        ),
    ]
