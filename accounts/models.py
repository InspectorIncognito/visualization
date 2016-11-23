from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static

class Carrier(models.Model):
    name = models.CharField(max_length=100)
    color_id = models.IntegerField(primary_key=True)
    image = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

class CarrierUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    carrier = models.ForeignKey(Carrier, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.user.username

    def string(self):
        return self.carrier.name

    def image(self):
        return self.carrier.image


class TransappUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __unicode__(self):
        return self.user.username

    def string(self):
        return self.user.username

    def image(self):
        return static("images/bus01.png")


class TransantiagoUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __unicode__(self):
        return self.user.username

    def string(self):
        return static("images/bus01.png")


