# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static
from django.db.models import Q

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

    def color(self):
        return Q(color_id=self.carrier.color_id)

    def isTransapp(self):
        return False

    @property
    def string(self):
        return self.carrier.name

    @property
    def image(self):
        return self.carrier.image


class TransappUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __unicode__(self):
        return self.user.username

    def isTransapp(self):
        return True

    def color(self):
        return Q()

    @property
    def string(self):
        return self.user.username.capitalize()

    @property
    def image(self):
        return static("carrier/images/bus01.png")


class TransantiagoUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __unicode__(self):
        return self.user.username

    def isTransapp(self):
        return False

    def color(self):
        return Q()

    @property
    def string(self):
        return self.user.username.capitalize()

    @property
    def image(self):
        return static("carrier/images/bus01.png")

class ProxyUser(User):
    class Meta:
        proxy = True

    def getUser(self):
        if hasattr(self, 'transappuser'):
            return self.transappuser
        elif hasattr(self, 'transantiagouser'):
            return self.transantiagouser
        elif hasattr(self, 'carrieruser'):
            return self.carrieruser
        else:
            return None