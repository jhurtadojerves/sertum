# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-20 15:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('centro', '0011_auto_20170118_1204'),
    ]

    operations = [
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(upload_to='')),
                ('center', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='centro.Center')),
            ],
        ),
    ]
