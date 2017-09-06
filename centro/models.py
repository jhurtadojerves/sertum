# -*- encoding: utf-8 -*-
from django.db import models
from django.urls import reverse

from autoslug import AutoSlugField

from django_google_maps import fields as map_fields
from django.core.validators import MinValueValidator, MaxValueValidator
from usuario.models import User

from multiselectfield import MultiSelectField

# Create your models here.


class Center(models.Model):
    name = models.TextField(blank=False)
    addres = map_fields.AddressField(max_length=200)
    aditional_information = models.TextField(blank=True, verbose_name='Place Description')
    geolocation = map_fields.GeoLocationField(max_length=100)
    slug = AutoSlugField(unique=True, populate_from='name', always_update=True)
    user = models.OneToOneField(User, unique=True, null=True)
    free = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('Center:center_detail', args=[self.slug, ])


class Picture(models.Model):
    picture = models.ImageField()
    center = models.ForeignKey(Center)


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

    group_type_choices = (
        ('0', 'Niños'),
        ('1', 'Adultos'),
        ('2', 'Adultos Mayores'),
    )

    activities_choices = (
        ('0', 'Observación de Paisajes'),
        ('1', 'Senderismo'),
        ('2', 'Contacto con la Naturaleza'),
        ('3', 'Visita Cultura'),
        ('4', 'Piscinas, Canchas, etc'),
        ('5', 'Canchas y Recreación')
    )

    transport_choices = (
        ('1', 'Transporte Público'),
        ('2', 'Transporte Privado'),
    )

    food_choices = (
        ('0', 'Comida Típica'),
        ('1', 'Platos a la Carta'),
        ('2', 'Menú del día')
    )

    # 1 =>
    group_type = models.ManyToManyField(GroupTypeForKnowledge)

    # 2 =>
    money_per_person = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[
            MinValueValidator(0),
        ]
    )

    # 3 =>
    activities = models.ManyToManyField(ActivityForKnowledge)

    # 4
    transport = models.ManyToManyField(TransportForKnowledge)

    # 5
    food = models.ManyToManyField(FoodForKnowledge)

class Poll(models.Model):
    user = models.ForeignKey(User, null=True)
    center = models.ForeignKey(Center, null=True)
    value = models.PositiveIntegerField(null=True)
    date = models.DateTimeField(auto_now_add=True)
