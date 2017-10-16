# -*- encoding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User as Usuario
from django.core.signals import request_finished
from django.dispatch import receiver
from django.db.models.signals import post_save


# Create your models here.

class User(models.Model):
    user = models.OneToOneField(Usuario, related_name='profile')
    has_add_center = models.BooleanField(default=False)
    reason_to_validate = models.TextField(blank=True)

    def __str__(self):
        return self.user.get_full_name()

    def get_full_name(self):
        return self.user.get_full_name()

    class Meta:
        permissions = (
            ('add_center', 'Puede Crear Centros Turísticos'),
        )
