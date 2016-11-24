from metars.models import Metar
from metars.serializers import MetarSerializer

from metars.workers.metar_decoder import MetarDecoder

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse

class MetarList (generics.ListCreateAPIView):
  queryset = Metar.objects.all()
  serializer_class = MetarSerializer

  def perform_create(self, serializer):
    decoder = MetarDecoder()
    decoder.decode_metar(self.request.data['raw_metar'])
    # serializer.save() # create a METAR resource

class MetarDetail(generics.CreateAPIView):
  queryset = Metar.objects.all()
  serializer_class = MetarSerializer
