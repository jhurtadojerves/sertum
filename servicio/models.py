# -*- encoding: utf-8 -*-

from django.db import models
from django.urls import reverse

from centro.models import Center


# Create your models here.

class Service(models.Model):
    name = models.TextField(blank=False)
    center = models.ForeignKey(Center, null=True)
    cost = models.DecimalField(max_digits=10,
                               decimal_places=2,
                               blank=False,
                               default=00.00)
    observation = models.TextField(blank=False,
                                   default=" ")

    def __str__(self):
        return self.name