from nose import with_setup
from nose.tools import assert_equals, assert_true

from metars.workers.metar_controller import MetarController
from metars.workers.parsers.default import MetarParserDefault
from metars.workers.decoders.default import MetarDecoderDefault
from metars.workers.parsers.nz import MetarParserNZ
from metars.workers.decoders.nz import MetarDecoderNZ

class TestMetarController:

  @classmethod
  def setup_class(cls):
    pass

  def test_parse_raw_metar_to_json(self):
    metar = 'METAR KHIO 290653Z AUTO 00000KT 10SM FEW032 OVC041 06/05 ' \
            'A3017 RMK AO2 RAB35E44 SLP219 P0000 T00560050'
    controller = MetarController()
    country = controller._get_country_from_raw_metar(metar)
    res = controller.parse_raw_metar_to_json(metar, country)
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
    assert_equals(res['stn_type'], "AO2")
    assert_equals(res['sea_level_pressure'], "SLP219")
    assert_equals(res['hourly_temp_dewpoint'], "T00560050")
    assert_equals(res['remarks'], "RAB35E44 P0000")
    assert_equals(res['misc'], "")

  ### Tests KHIO, 24-Dec-16 with low vis. Found a bug with METAR parser
  ### not handling vertical visibility sky condition.
  def test_parse_raw_metar_to_json_khio_24_dec_16(self):
    metar = 'METAR KHIO 241953Z 00000KT 1/4SM R13R/1200V1800FT FG VV002 ' \
            '00/M01 A2996 RMK AO2 SLP150 T00001006'
    controller = MetarController()
    country = controller._get_country_from_raw_metar(metar)
    res = controller.parse_raw_metar_to_json(metar, country)
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
    assert_equals(res['stn_type'], "AO2")
    assert_equals(res['sea_level_pressure'], "SLP150")
    assert_equals(res['hourly_temp_dewpoint'], "T00001006")
    assert_equals(res['remarks'], "")
    assert_equals(res['misc'], '')

  def test_parse_raw_metar_to_json_khio_31_mar_17(self):
    metar = 'KHIO 010053Z 00000KT 10SM CLR 14/06 A3026 RMK AO2 SLP247 T01440056'
    controller = MetarController()
    country = controller._get_country_from_raw_metar(metar)
    res = controller.parse_raw_metar_to_json(metar, country)
    assert_equals(res['is_special_report'], False)
    assert_equals(res['icao_id'], "KHIO")
    assert_equals(res['obs_datetime'], "010053Z")
    assert_equals(res['mod_auto'], False)
    assert_equals(res['wind_dir_speed'], "00000KT")
    assert_equals(res['wind_dir_variation'], "")
    assert_equals(res['vis'], "10SM")
    assert_equals(res['sky_condition'], ["CLR"])
    assert_equals(res['temp'], "14")
    assert_equals(res['dewpoint'], "06")
    assert_equals(res['altimeter'], "3026")
    assert_equals(res['sea_level_pressure'], "SLP247")
    assert_equals(res['hourly_temp_dewpoint'], "T01440056")
    assert_equals(res['remarks'], "")
    assert_equals(res['misc'], '')

  def test_parse_raw_metar_to_json_ksql_20_jun_17(self):
    metar = 'KSQL 201455Z VRB03KT 10SM SKC 19/14 A2987'
    controller = MetarController()
    country = controller._get_country_from_raw_metar(metar)
    res = controller.parse_raw_metar_to_json(metar, country)
    assert_equals(res['is_special_report'], False)
    assert_equals(res['icao_id'], "KSQL")
    assert_equals(res['obs_datetime'], "201455Z")
    assert_equals(res['mod_auto'], False)
    assert_equals(res['wind_dir_speed'], "VRB03KT")
    assert_equals(res['wind_dir_variation'], "")
    assert_equals(res['vis'], "10SM")
    assert_equals(res['sky_condition'], ["SKC"])
    assert_equals(res['temp'], "19")
    assert_equals(res['dewpoint'], "14")
    assert_equals(res['altimeter'], "2987")
    assert_equals(res['remarks'], "")

  def test_get_country_from_raw_metar_us(self):
    metar = 'KPDX 300453Z 31009KT 10SM FEW250 22/14 A3004'
    controller = MetarController()
    res = controller._get_country_from_raw_metar(metar)
    assert_equals(res, 'US')

  def test_get_country_from_raw_metar_nz(self):
    metar = 'NZWN 300530Z AUTO 36014KT 9999'
    controller = MetarController()
    res = controller._get_country_from_raw_metar(metar)
    assert_equals(res, 'NZ')

  def test_get_parser_for_country_us(self):
    controller = MetarController()
    parser = controller._get_parser_for_country('US')
    assert_true(isinstance(parser, MetarParserDefault))

  def test_get_decoder_for_country_us(self):
    controller = MetarController()
    decoder = controller._get_decoder_for_country('US')
    assert_true(isinstance(decoder, MetarDecoderDefault))

  def test_get_parser_for_country_nz(self):
    controller = MetarController()
    parser = controller._get_parser_for_country('NZ')
    assert_true(isinstance(parser, MetarParserNZ))

  def test_get_decoder_for_country_nz(self):
    controller = MetarController()
    decoder = controller._get_decoder_for_country('NZ')
    assert_true(isinstance(decoder, MetarDecoderNZ))
