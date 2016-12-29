from nose import with_setup
from nose.tools import assert_equals

from metars.workers.metar_controller import MetarController

class TestMetarController:

  @classmethod
  def setup_class(cls):
    pass

  def test_parse_raw_metar_to_json(self):
    metar = 'METAR KHIO 290653Z AUTO 00000KT 10SM FEW032 OVC041 06/05 ' \
            'A3017 RMK AO2 RAB35E44 SLP219 P0000 T00560050'
    controller = MetarController()
    res = controller.parse_raw_metar_to_json(metar)
    assert_equals(res['is_special_report'], False)
    assert_equals(res['icao_id'], "KHIO")
    assert_equals(res['obs_datetime'], "290653Z")
    assert_equals(res['mod_auto'], True)
    assert_equals(res['wind_dir_speed'], "00000KT")
    assert_equals(res['wind_dir_variation'], "")
    assert_equals(res['vis'], "10SM")
    assert_equals(res['rvr'], "")
    assert_equals(res['wx_phenomena'], [])
    assert_equals(res['sky_condition'], ["FEW032", "OVC041"])
    assert_equals(res['temp'], "06")
    assert_equals(res['dewpoint'], "05")
    assert_equals(res['altimeter'], "3017")
    assert_equals(res['remarks'], "RMK AO2 RAB35E44 SLP219 P0000 T00560050")

  ### Tests KHIO, 24-Dec-16 with low vis. Found a bug with METAR parser
  ### not handling vertical visibility sky condition.
  def test_parse_raw_metar_to_json_khio_24_dec_16(self):
    metar = 'METAR KHIO 241953Z 00000KT 1/4SM R13R/1200V1800FT FG VV002 ' \
            '00/M01 A2996 RMK AO2 SLP150 T00001006'
    controller = MetarController()
    res = controller.parse_raw_metar_to_json(metar)
    assert_equals(res['is_special_report'], False)
    assert_equals(res['icao_id'], "KHIO")
    assert_equals(res['obs_datetime'], "241953Z")
    assert_equals(res['mod_auto'], False)
    assert_equals(res['wind_dir_speed'], "00000KT")
    assert_equals(res['wind_dir_variation'], "")
    assert_equals(res['vis'], "1/4SM")
    assert_equals(res['rvr'], "R13R/1200V1800FT")
    assert_equals(res['wx_phenomena'], ["FG"])
    assert_equals(res['sky_condition'], ["VV002"])
    assert_equals(res['temp'], "00")
    assert_equals(res['dewpoint'], "M01")
    assert_equals(res['altimeter'], "2996")
    assert_equals(res['remarks'], "RMK AO2 SLP150 T00001006")
