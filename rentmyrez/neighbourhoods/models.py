from __future__ import unicode_literals

from django.db import models
from jsonfield import JSONField

class Neighbourhood(models.Model):
    name = models.CharField(max_length=100, unique=True)
    boundary = JSONField()
