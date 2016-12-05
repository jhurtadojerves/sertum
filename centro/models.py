# -*- encoding: utf-8 -*-
from django.db import models

from autoslug import AutoSlugField

from django_google_maps import fields as map_fields
from django.core.validators import MinValueValidator, MaxValueValidator
from servicio.models import Service

# Create your models here.

class Center(models.Model):
    name = models.TextField(blank=False)
    addres = map_fields.AddressField(max_length=200)
    geolocation = map_fields.GeoLocationField(max_length=100)
    slug = AutoSlugField(unique=True, populate_from='name', always_update=True)

    def __str__(self):
        return self.name
