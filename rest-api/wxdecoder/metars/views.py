from metars.models import Metar
from metars.serializers import MetarSerializer

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse

class MetarDetail(generics.CreateAPIView):
  queryset = Metar.objects.all()
  serializer_class = MetarSerializer

  def perform_create(self, MetarSerializer):
    print 'something!'
