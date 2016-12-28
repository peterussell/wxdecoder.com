from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from metars.models import Metar
from metars.serializers import MetarSerializer
from metars.workers.metar_controller import MetarController


class DecodeMetar(APIView):
  """
  Decodes METAR text submitted with the request and returns the decoded METAR.
  """
  def get(self, request, format=None):
    controller = MetarController()
    try:
      decoded = controller.decode_metar(request.data['raw_metar'])
    except Exception as e:
      print "> Exception: %s" % e.message
      return Response("Failed to decode METAR.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response({ 'decoded_metar': decoded })


class RetrieveAndDecodeMetar(APIView):
  """
  Retrieves the METAR for the provided airport identifier, decodes and returns it.
  """
  def get(self, request, airport_id, format=None):
    controller = MetarController()
#    try:
    decoded = controller.retrieve_and_decode_metar(airport_id)
#    except Exception as e:
#      return Response("Failed to decode METAR.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response({ 'decoded_metar': decoded })
