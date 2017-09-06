# -*- encoding: utf-8 -*-

from django.db import models
from django.urls import reverse

from centro.models import Center
from autoslug import AutoSlugField


# Create your models here.

class Service(models.Model):
    name_choices = (
        ('Piscinas', 'Piscinas'),
        ('Balneario', 'Balneario'),
        ('Mirador', 'Mirador'),
        ('Senderismo', 'Senderismo'),
        ('Canchas Deportivas', 'Canchas Deportivas'),
        ('Mirador', 'Mirador'),
        ('Bar Nocturno', 'Bar Nocturno'),
        ('Alojamiento', 'Alojamiento'),
        ('Restaurante', 'Resturante'),
        ('Cabañas', 'Cabañas'),
        ('Asadero', 'Asadero'),
        ('Pesca Deportiva', 'Pesca Deportiva'),
        ('Servicios Culturales', 'Servicios Culturales'),
        ('Dique', 'Dique'),
        ('Canotaje', 'Canotaje'),
        ('Rafting', 'Rafting'),
        ('Canopy', 'Canopy'),
    )

    name = models.CharField(max_length=256, choices=name_choices)
    slug = AutoSlugField(populate_from='name', always_update=True, null=True, default=None)
    center = models.ForeignKey(Center, null=True)
    cost = models.DecimalField(max_digits=10,
                               decimal_places=2,
                               blank=False,
                               default=00.00)
    observation = models.TextField(blank=False,
                                   default=" ")

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ['name', 'center']
