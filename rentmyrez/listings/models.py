from __future__ import unicode_literals

from django.db import models

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

    class Meta:
        ordering = ('date_listed',)
