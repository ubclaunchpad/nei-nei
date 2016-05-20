from __future__ import unicode_literals

from django.db import models
import uuid

class House(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    num_bedrooms = models.IntegerField()
    square_footage = models.IntegerField()
    rent = models.IntegerField()
    posted = models.DateField()
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __unicode__(self):
        return self.uuid
