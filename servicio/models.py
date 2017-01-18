# -*- encoding: utf-8 -*-

from django.db import models
from django.urls import reverse

# Create your models here.

class Service(models.Model):
    name = models.TextField(blank=False)

    def __str__(self):
        return self.name