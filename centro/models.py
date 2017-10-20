# -*- encoding: utf-8 -*-
from django.db import models
from django.urls import reverse

from autoslug import AutoSlugField

from django_google_maps import fields as map_fields
from django.core.validators import MinValueValidator, MaxValueValidator
from usuario.models import User
from servicio.models import Service

from multiselectfield import MultiSelectField

# Create your models here.


class Center(models.Model):
    name = models.TextField(blank=False)
    addres = map_fields.AddressField(max_length=200)
    aditional_information = models.TextField(blank=True, verbose_name='Place Description')
    geolocation = map_fields.GeoLocationField(max_length=100)
    slug = AutoSlugField(unique=True, populate_from='name', always_update=True)
    user = models.OneToOneField(User, unique=True, null=True, related_name='center')
    free = models.BooleanField(default=False)
    service = models.ManyToManyField(Service, through='ServiceCenter')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('Center:center_detail', args=[self.slug, ])

    def save(self, *args, **kwargs):
        self.geolocation = self.addres
        super().save(*args, **kwargs)


class Picture(models.Model):
    picture = models.ImageField()
    center = models.ForeignKey(Center, related_name='pictures')
    description = models.CharField(max_length=255)


class ActivityForKnowledge(models.Model):
    name = models.TextField(blank=False, unique=True)

    def __str__(self):
        return self.name


class GroupTypeForKnowledge(models.Model):
    name = models.TextField(blank=False, unique=True)

    def __str__(self):
        return self.name


class FoodForKnowledge(models.Model):
    name = models.TextField(blank=False, unique=True)

    def __str__(self):
        return self.name


class TransportForKnowledge(models.Model):
    name = models.TextField(blank=False, unique=True)

    def __str__(self):
        return self.name


class Knowledge(models.Model):
    center = models.ForeignKey(Center, unique=True)
    group_type = models.ManyToManyField(GroupTypeForKnowledge)
    money_per_person = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[
            MinValueValidator(0),
        ]
    )
    activities = models.ManyToManyField(ActivityForKnowledge)
    transport = models.ManyToManyField(TransportForKnowledge)
    food = models.ManyToManyField(FoodForKnowledge)


class Poll(models.Model):
    user = models.ForeignKey(User, null=True)
    center = models.ForeignKey(Center, null=True)
    value = models.PositiveIntegerField(null=True)
    date = models.DateTimeField(auto_now_add=True)


class ServiceCenter(models.Model):
    center = models.ForeignKey(Center)
    service = models.ForeignKey(Service)

    cost = models.DecimalField(max_digits=10,
                               decimal_places=2,
                               blank=False,
                               default=00.00)
    observation = models.TextField(blank=True)

    def __str__(self):
        return self.service.name