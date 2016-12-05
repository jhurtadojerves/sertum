# -*- encoding: utf-8 -*-
from django.db import models


from slughifi import slughifi
from django_google_maps import fields as map_fields
from django.core.validators import MinValueValidator, MaxValueValidator
from servicio.models import Service

# Create your models here.

class Center(models.Model):
    name = models.TextField(blank=False)
    addres = map_fields.AddressField(max_length=200)
    geolocation = map_fields.GeoLocationField(max_length=100)
    slug = models.SlugField(max_length=100)

    def save(self, *args, **kwargs):
        self.slug = slughifi(self.name)
        super(Center, self).save(*args,**kwargs)

    def __str__(self):
        return self.name
