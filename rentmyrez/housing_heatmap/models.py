from __future__ import unicode_literals

from django.db import models
import uuid

class House(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    num_bedrooms = models.IntegerField()
    square_footage = models.IntegerField(default=0)
    posting_url = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    rent = models.IntegerField()
    posted = models.DateField(null=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __unicode__(self):
        to_string = ', '.join([str(self.latitude), str(self.longitude)])
        return to_string
