# -*- encoding: utf-8 -*-
from django.db import models
from django.urls import reverse

from autoslug import AutoSlugField

from django_google_maps import fields as map_fields
from django.core.validators import MinValueValidator, MaxValueValidator
from usuario.models import User



# Create your models here.

class Center(models.Model):
    name = models.TextField(blank=False)
    addres = map_fields.AddressField(max_length=200)
    aditional_information = models.TextField(blank=True)
    geolocation = map_fields.GeoLocationField(max_length=100)
    slug = AutoSlugField(unique=True, populate_from='name', always_update=True)
    user = models.OneToOneField(User, unique=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('Center:center_detail', args=[self.slug,])

'''class CenterService(models.Model):
    center = models.ForeignKey(Center)
    service = models.ForeignKey(Service)
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    observation = models.TextField(blank=False)

    class Meta:
        unique_together = ('center', 'service',)

    def __str__(self):
        return self.center.name
'''

class Picture(models.Model):
    picture = models.ImageField()
    center = models.ForeignKey(Center)