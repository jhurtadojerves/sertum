# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-22 14:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0003_auto_20170122_0952'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'permissions': (('as_premium', 'Puede Crear Centros Turísticos'),)},
        ),
    ]