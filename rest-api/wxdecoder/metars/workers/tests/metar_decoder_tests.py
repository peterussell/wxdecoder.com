from nose import with_setup
from nose.tools import assert_equals
import json

from metars.workers.metar_decoder import MetarDecoder

class TestMetarController:

  @classmethod
  def setup_class(cls):
    pass

  def test_decode_metar(self):
    with open('tests/data/khio_encoded.json') as data:
      khio = json.load(data)
    print khio
