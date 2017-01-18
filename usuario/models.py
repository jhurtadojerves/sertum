# -*- encoding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class User(models.Model):
    user = models.OneToOneField(User)
    type_choices = (
        ('u', 'Usuario Normal'),
        ('c', 'Usuario Centro'),
    )
    type = models.CharField(max_length=1, choices=type_choices, default='u')

    def __str__(self):
        return self.user.get_full_name()


    def as_premium(self):
        if(self.type == 'c'):
            return True
        else:
            return False