from email.policy import default
from types import CoroutineType
from unicodedata import name
from django.db import models

class standort_restaurant(models.Model):
    first_name = models.CharField(max_length=200, default='none')
    last_name = models.CharField(max_length=200, default='none')
    restaurant_name = models.CharField(max_length=200)
    #address = models.CharField(max_length=200)
    #lat = models.DecimalField(max_digits=10, decimal_places=8)
    #lon = models.DecimalField(max_digits=11, decimal_places=8)
    #country = models.CharField(max_length=200, default='default value')
    #email = models.CharField(max_length=200, default='default value')
    #verified = models.BooleanField(default=False)
    #menu = models.BooleanField(default=False)

    def __str__(self):
        return self.restaurant_name
