# -*- encoding: utf-8 -*-

from django.db import models
from django.urls import reverse

from autoslug import AutoSlugField


# Create your models here.

class Service(models.Model):

    name = models.CharField(max_length=256, unique=True)
    slug = AutoSlugField(unique=True, populate_from='name', always_update=True, null=True, default=name)

    def __str__(self):
        return self.name
