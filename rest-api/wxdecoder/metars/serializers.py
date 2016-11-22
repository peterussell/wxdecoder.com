from rest_framework import serializers

from metars.models import Metar

class MetarSerializer(serializers.ModelSerializer):

  class Meta:
    model = Metar
    fields = ('id', 'raw_metar')
