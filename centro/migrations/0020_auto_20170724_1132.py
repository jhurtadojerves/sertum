# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-07-24 16:32
from __future__ import unicode_literals

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('centro', '0019_poll'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='food',
            field=models.CharField(choices=[('0', 'Comida Típica'), ('1', 'Platos a la Carta'), ('2', 'Menú del día'), ('3', 'No comida')], default=1, max_length=1),
        ),
        migrations.AlterField(
            model_name='poll',
            name='group_type',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('0', 'Niños'), ('1', 'Adultos'), ('2', 'Adultos Mayores')], default='0', max_length=1),
        ),
        migrations.AlterField(
            model_name='poll',
            name='transport',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('0', 'Transporte Público'), ('1', 'Transporte Privado')], default='0', max_length=1),
        ),
    ]
