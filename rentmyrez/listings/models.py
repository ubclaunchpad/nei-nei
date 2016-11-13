from __future__ import unicode_literals

from django.db import models
from jsonfield import JSONField
from django.core.validators import MaxValueValidator, MinValueValidator


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

class HistoricalListings(models.Model):
    week = models.IntegerField(primary_key=True, validators=[
        MaxValueValidator(51),
        MinValueValidator(0)
    ])
    neighbourhood_name = models.CharField(max_length=100)
    average_price = models.IntegerField(default=0)
    median_price = models.IntegerField(default=0)
    first_q_price = models.IntegerField(default=0)
    third_q_price = models.IntegerField(default=0)
    range_price = models.IntegerField(default=0)
    average_bedrooms = models.IntegerField(null=True)
    exp_moving_average_price = models.IntegerField(default=0)
    neighbourhood = models.ForeignKey(Neighbourhood, null=True, on_delete=models.CASCADE, related_name='historical_listings')




