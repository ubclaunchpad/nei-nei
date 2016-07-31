from __future__ import unicode_literals

from django.db import models
from jsonfield import JSONField

class Neighbourhood(models.Model):
    name = models.CharField(max_length=100, unique=True)
    boundary = JSONField()

    __unicode__ = lambda self: self.name

class Listing(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    description = models.TextField()
    listing_url = models.CharField(max_length=250, unique=True)
    listing_id = models.IntegerField(unique=True)
    address = models.CharField(max_length=100)
    price = models.IntegerField()
    date_listed = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    neighbourhood = models.ForeignKey(Neighbourhood, null=True, on_delete=models.CASCADE, related_name='listings')

    class Meta:
        ordering = ('date_listed',)
