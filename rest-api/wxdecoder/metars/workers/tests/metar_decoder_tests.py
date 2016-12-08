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
    decoder = MetarDecoder()
    decoder.decode_metar(khio["metar"])

  def test_decode_is_special_report(self):
    val = True
    decoder = MetarDecoder()
    decoder.decode_is_special_report(val)
    res = decoder.decoded_metar["is_special_report"]["decoded"]
    assert_equals(res, True)

  def test_decode_is_not_special_report(self):
    val = False
    decoder = MetarDecoder()
    decoder.decode_is_special_report(val)
    res = decoder.decoded_metar["is_special_report"]["decoded"]
    assert_equals(res, False)

  def test_decode_icao_id(self):
    val = "KPDX"
    decoder = MetarDecoder()
    decoder.decode_icao_id(val)
    res = decoder.decoded_metar["icao_id"]["decoded"]
    assert_equals(res, "KPDX")

  def test_decode_obs_datetime(self):
    val = "290653Z"
    decoder = MetarDecoder()
    decoder.decode_obs_datetime(val)
    res_date = decoder.decoded_metar["obs_datetime"]["decoded"]["date"]
    res_time = decoder.decoded_metar["obs_datetime"]["decoded"]["time"]
    assert_equals(res_date, "29")
    assert_equals(res_time, "0653")

  def test_decode_is_automated(self):
    val = True
    decoder = MetarDecoder()
    decoder.decode_mod_auto(val)
    res = decoder.decoded_metar["mod_auto"]["decoded"]
    assert_equals(res, True)

  def test_decode_is_not_automated(self):
    val = False
    decoder = MetarDecoder()
    decoder.decode_mod_auto(val)
    res = decoder.decoded_metar["mod_auto"]["decoded"]
    assert_equals(res, False)
