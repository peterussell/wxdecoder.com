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
    assert_equals(res['altimeter'], "A3017")
    assert_equals(res['remarks'], "RMK AO2 RAB35E44 SLP219 P0000 T00560050")
