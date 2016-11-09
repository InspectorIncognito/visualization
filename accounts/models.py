from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

class Carrier(models.Model):
    name = models.CharField(max_length=100)
    color_id = models.IntegerField()
    image = models.CharField(max_length=200)

class CarrierUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    carrier = models.ForeignKey(Carrier, on_delete=models.CASCADE)


