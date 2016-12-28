from __future__ import unicode_literals

from django.db import models

class Metar(models.Model):
  raw_metar = models.TextField()
  decoded_metar = models.TextField()
  #decoded_metar = models.TextField()
  #issued_at = models.DateTimeField()
  #airport_id = models.CharField(max_length=10, blank=True, default='')

  class Meta:
    #ordering = ('airport_id',)
    ordering = ('raw_metar',)
