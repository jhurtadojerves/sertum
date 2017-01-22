# -*- encoding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class User(models.Model):
    user = models.OneToOneField(User)

    def __str__(self):
        return self.user.get_full_name()

    def get_full_name(self):
        return self.user.get_full_name()

    class Meta:
        permissions = (
            ('add_center', 'Puede Crear Centros Turísticos'),
        )