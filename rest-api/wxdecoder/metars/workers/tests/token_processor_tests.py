from nose import with_setup
from nose.tools import assert_equals

from metars.workers.metar_decoder import MetarDecoder

class TestTokenProcessor:

  @classmethod
  def setup_class(cls):
    cls.metar = 'METAR KHIO 290653Z AUTO 00000KT 10SM FEW032 OVC041 06/05 A3017 RMK AO2 ' \
                'RAB35E44 SLP219 P0000 T00560050'
    cls.tokens = cls.metar.split()

  ### Test Individual Token Processors
  def test_process_metar_header_with_metar_header(self):
    decoder = MetarDecoder()
    tokens = 'METAR KHIO'.split()
    res = decoder.process_metar_header(tokens)
    assert_equals(res[0], 'KHIO')

  def test_process_metar_header_without_metar_header(self):
    decoder = MetarDecoder()
    tokens = 'KHIO 290653Z'.split()
    res = decoder.process_metar_header(tokens)
    assert_equals(res, ['KHIO', '290653Z'])

  def test_process_icao_id(self):
    decoder = MetarDecoder()
    tokens = 'KHIO 290653Z'.split()
    res = decoder.process_icao_id(tokens)
    assert_equals(decoder.icao_id, 'KHIO')
    assert_equals(tokens[0], '290653Z')

  @classmethod
  def teardown_class(cls):
    pass
