from nose import with_setup
from nose.tools import assert_equals

from metars.workers.metar_parser import MetarParser

class TestMetarParser:

  @classmethod
  def setup_class(cls):
    pass

  ### Test full token parseor
  def test_parse_metar_khio(self):
    metar = 'METAR KHIO 290653Z AUTO 00000KT 10SM FEW032 OVC041 06/05 ' \
            'A3017 RMK AO2 RAB35E44 SLP219 P0000 T00560050'
    parser = MetarParser()
    res = parser.parse_tokens(metar.split())
    assert_equals(parser.parsed_metar["is_special_report"], False)
    assert_equals(parser.parsed_metar["icao_id"], 'KHIO')
    assert_equals(parser.parsed_metar["obs_datetime"], '290653Z')
    assert_equals(parser.parsed_metar["mod_auto"], True)
    assert_equals(parser.parsed_metar["wind_dir_speed"], '00000KT')
    assert_equals(parser.parsed_metar["vis"], '10SM')
    assert_equals(parser.parsed_metar["wx_phenomena"], [])
    assert_equals(parser.parsed_metar["sky_condition"], ['FEW032', 'OVC041'])
    assert_equals(parser.parsed_metar["temp"], '06')
    assert_equals(parser.parsed_metar["dewpoint"], '05')
    assert_equals(parser.parsed_metar["altimeter"], 'A3017')
    assert_equals(parser.parsed_metar["remarks"], 'RMK AO2 RAB35E44 SLP219 P0000 T00560050')

  ### Test Individual Token Processors
  def test_parse_metar_header_with_metar_header(self):
    parser = MetarParser()
    tokens = 'METAR KHIO'.split()
    res = parser.parse_metar_header(tokens)
    assert_equals(res[0], 'KHIO')

  def test_parse_metar_header_without_metar_header(self):
    parser = MetarParser()
    tokens = 'KHIO 290653Z'.split()
    res = parser.parse_metar_header(tokens)
    assert_equals(res, ['KHIO', '290653Z'])

  def test_parse_icao_id(self):
    parser = MetarParser()
    tokens = 'KHIO 290653Z'.split()
    res = parser.parse_icao_id(tokens)
    assert_equals(parser.parsed_metar["icao_id"], 'KHIO')
    assert_equals(res[0], '290653Z')

  def test_parse_datetime(self):
    parser = MetarParser()
    tokens = '290653Z AUTO'.split()
    res = parser.parse_datetime(tokens)
    assert_equals(parser.parsed_metar["obs_datetime"], '290653Z')
    assert_equals(res[0], 'AUTO')

  def test_parse_automated_obs_flag_with_flag(self):
    parser = MetarParser()
    tokens = 'AUTO 00000KT'.split()
    res = parser.parse_automated_obs_flag(tokens)
    assert_equals(parser.parsed_metar["mod_auto"], True)
    assert_equals(res[0], '00000KT')

  def test_parse_automated_obs_flag_without_flag(self):
    ### If the AUTO flag is missing from the METAR, the obs_datetime
    ### field should be false and nothing stripped from the METAR
    parser = MetarParser()
    tokens = '290653Z 00000KT'.split()
    res = parser.parse_automated_obs_flag(tokens)
    assert_equals(parser.parsed_metar["mod_auto"], False)
    assert_equals(res, ['290653Z', '00000KT'])

  def test_parse_winds_calm(self):
    parser = MetarParser()
    tokens = '00000KT 10SM'.split()
    res = parser.parse_wind_dir_speed(tokens)
    assert_equals(parser.parsed_metar["wind_dir_speed"], '00000KT')
    assert_equals(res, ['10SM'])

  def test_parse_winds_light_variable(self):
    parser = MetarParser()
    tokens = 'VRB005KT'.split()
    res = parser.parse_wind_dir_speed(tokens)
    assert_equals(parser.parsed_metar["wind_dir_speed"], 'VRB005KT')

  def test_parse_winds_basic(self):
    parser = MetarParser()
    tokens = '18004KT 10SM'.split()
    res = parser.parse_wind_dir_speed(tokens)
    assert_equals(parser.parsed_metar["wind_dir_speed"], '18004KT')

  def test_parse_winds_with_gusts(self):
    parser = MetarParser()
    tokens = '21016G24KT 10SM'.split()
    res = parser.parse_wind_dir_speed(tokens)
    assert_equals(parser.parsed_metar["wind_dir_speed"], '21016G24KT')

  def test_parse_winds_variable(self):
    parser = MetarParser()
    tokens = '18015KT 150V210 10SM'.split()
    # Make sure both the wind info and direction variation get picked up
    res = parser.parse_wind_dir_speed(tokens)
    res = parser.parse_wind_dir_variation(res)
    assert_equals(parser.parsed_metar["wind_dir_speed"], '18015KT')
    assert_equals(parser.parsed_metar["wind_dir_variation"], '150V210')

  def test_parse_winds_variable_missing(self):
    ### If the variable winds section is missing we shouldn't set the
    ### MetarParser's wind_dir_variation field, or strip anything
    parser = MetarParser()
    tokens = '18015KT 10SM'.split()
    # Include the wind_dir_speed parseor for a sanity check
    res = parser.parse_wind_dir_speed(tokens)
    res = parser.parse_wind_dir_variation(res)
    assert_equals(parser.parsed_metar["wind_dir_speed"], '18015KT')
    assert_equals(parser.parsed_metar["wind_dir_variation"], '')
    assert_equals(res, ['10SM'])

  def test_parse_visibility(self):
    parser = MetarParser()
    tokens = '10SM R11/P6000FT'.split()
    res = parser.parse_visibility(tokens)
    assert_equals(parser.parsed_metar["vis"], '10SM')
    assert_equals(res[0], 'R11/P6000FT')

  def test_parse_visibility_missing(self):
    ### If the visibility field is missing, the MetarParser's 'vis' field
    ### should remain unset and nothing stripped from the METAR
    parser = MetarParser()
    tokens = '21016G24KT R11/P6000FT'.split()
    res = parser.parse_visibility(tokens)
    assert_equals(parser.parsed_metar["vis"], '')
    assert_equals(res, ['21016G24KT', 'R11/P6000FT'])

  def test_parse_rvr(self):
    parser = MetarParser()
    tokens = 'R11/P6000FT -RA BR'.split()
    res = parser.parse_rvr(tokens)
    assert_equals(parser.parsed_metar["rvr"], 'R11/P6000FT')
    assert_equals(res, ['-RA', 'BR'])

  def test_parse_rvr_missing(self):
    ### If the RVR is missing, the MetarParser's 'rvr' field should
    ### remain unset and nothing stripped from the METAR
    parser = MetarParser()
    tokens = 'VRB005 -RA BR'.split()
    res = parser.parse_rvr(tokens)
    assert_equals(parser.parsed_metar["rvr"], '')
    assert_equals(res, ['VRB005', '-RA', 'BR'])

  def test_parse_rvr_missing_with_similar_wx_phenomena(self):
    ### The RVR field begins with 'R', but the following WX phenomena
    ### section can also start with 'R' in the case of moderate rain: 'RA'.
    ### This test ensures we don't mis-identify 'RA' as the RVR field.
    parser = MetarParser()
    tokens = '18015KT RA'.split()
    res = parser.parse_wind_dir_speed(tokens)
    res = parser.parse_rvr(res)
    assert_equals(parser.parsed_metar["rvr"], '')
    assert_equals(res, ['RA'])

  def test_parse_wx_phenomena(self):
    parser = MetarParser()
    tokens = '-RA BR BKN015 OVC025'.split()
    res = parser.parse_wx_phenomena(tokens)
    assert_equals(parser.parsed_metar["wx_phenomena"], ['-RA', 'BR'])
    assert_equals(res, ['BKN015', 'OVC025'])

  def test_parse_wx_phenomena_missing(self):
    parser = MetarParser()
    tokens = 'FEW020 SCT150'.split()
    res = parser.parse_wx_phenomena(tokens)
    assert_equals(parser.parsed_metar["wx_phenomena"], [])
    assert_equals(res, ['FEW020', 'SCT150'])

  def test_parse_sky_condition(self):
    parser = MetarParser()
    tokens = 'BKN015 OVC025 06/04'.split()
    res = parser.parse_sky_condition(tokens)
    assert_equals(parser.parsed_metar["sky_condition"], ['BKN015', 'OVC025'])
    assert_equals(res, ['06/04'])

  def test_parse_sky_condition_missing(self):
    parser = MetarParser()
    tokens = '06/04 A2990'.split()
    res = parser.parse_sky_condition(tokens)
    assert_equals(parser.parsed_metar["sky_condition"], [])
    assert_equals(res, ['06/04', 'A2990'])

  def test_parse_tmp_dewpoint(self):
    parser = MetarParser()
    tokens = '06/04 A2990'.split()
    res = parser.parse_temp_dewpoint(tokens)
    assert_equals(parser.parsed_metar["temp"], '06')
    assert_equals(parser.parsed_metar["dewpoint"], '04')
    assert_equals(res, ['A2990'])

  def test_parse_temp_dewpoint_missing(self):
    parser = MetarParser()
    tokens = 'A2990 RMK'.split()
    res = parser.parse_temp_dewpoint(tokens)
    assert_equals(parser.parsed_metar["temp"], '')
    assert_equals(parser.parsed_metar["dewpoint"], '')
    assert_equals(res, ['A2990', 'RMK'])

  def test_parse_altimeter(self):
    parser = MetarParser()
    tokens = 'A2990 RMK'.split()
    res = parser.parse_altimeter(tokens)
    assert_equals(parser.parsed_metar["altimeter"], 'A2990')
    assert_equals(res, ['RMK'])

  def test_parse_altimeter_missing(self):
    parser = MetarParser()
    tokens = 'RMK TORNADO'.split()
    res = parser.parse_altimeter(tokens)
    assert_equals(parser.parsed_metar["altimeter"], '')
    assert_equals(res, ['RMK', 'TORNADO'])

  @classmethod
  def teardown_class(cls):
    pass