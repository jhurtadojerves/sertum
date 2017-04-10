# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-04-10 14:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('centro', '0015_auto_20170410_0915'),
        ('servicio', '0003_auto_20161211_1648'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='center',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='centro.Center'),
        ),
        migrations.AddField(
            model_name='service',
            name='cost',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='service',
            name='observation',
            field=models.TextField(default=' '),
        ),
    ]