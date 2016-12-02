from nose import with_setup
from nose.tools import assert_equals

from metars.workers.metar_decoder import MetarDecoder

class TestTokenProcessor:

  @classmethod
  def setup_class(cls):
    pass

  ### Test full token processor
  def test_process_metar_khio(self):
    metar = 'METAR KHIO 290653Z AUTO 00000KT 10SM FEW032 OVC041 06/05 ' \
            'A3017 RMK AO2 RAB35E44 SLP219 P0000 T00560050'
    decoder = MetarDecoder()
    res = decoder.process_tokens(metar.split())
    assert_equals(decoder.is_special_report, False)
    assert_equals(decoder.icao_id, 'KHIO')
    assert_equals(decoder.obs_datetime, '290653Z')
    assert_equals(decoder.mod_auto, True)
    assert_equals(decoder.wind_dir_speed, '00000KT')
    assert_equals(decoder.vis, '10SM')
    assert_equals(decoder.wx_phenomena, [])
    assert_equals(decoder.sky_condition, ['FEW032', 'OVC041'])
    assert_equals(decoder.temp, '06')
    assert_equals(decoder.dewpoint, '05')
    assert_equals(decoder.altimeter, 'A3017')
    assert_equals(decoder.remarks, 'RMK AO2 RAB35E44 SLP219 P0000 T00560050')

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
    assert_equals(res[0], '290653Z')

  def test_process_datetime(self):
    decoder = MetarDecoder()
    tokens = '290653Z AUTO'.split()
    res = decoder.process_datetime(tokens)
    assert_equals(decoder.obs_datetime, '290653Z')
    assert_equals(res[0], 'AUTO')

  def test_process_automated_obs_flag_with_flag(self):
    decoder = MetarDecoder()
    tokens = 'AUTO 00000KT'.split()
    res = decoder.process_automated_obs_flag(tokens)
    assert_equals(decoder.mod_auto, True)
    assert_equals(res[0], '00000KT')

  def test_process_automated_obs_flag_without_flag(self):
    ### If the AUTO flag is missing from the METAR, the obs_datetime
    ### field should be false and nothing stripped from the METAR
    decoder = MetarDecoder()
    tokens = '290653Z 00000KT'.split()
    res = decoder.process_automated_obs_flag(tokens)
    assert_equals(decoder.mod_auto, False)
    assert_equals(res, ['290653Z', '00000KT'])

  def test_process_winds_calm(self):
    decoder = MetarDecoder()
    tokens = '00000KT 10SM'.split()
    res = decoder.process_wind_dir_speed(tokens)
    assert_equals(decoder.wind_dir_speed, '00000KT')
    assert_equals(res, ['10SM'])

  def test_process_winds_light_variable(self):
    decoder = MetarDecoder()
    tokens = 'VRB005KT'.split()
    res = decoder.process_wind_dir_speed(tokens)
    assert_equals(decoder.wind_dir_speed, 'VRB005KT')

  def test_process_winds_basic(self):
    decoder = MetarDecoder()
    tokens = '18004KT 10SM'.split()
    res = decoder.process_wind_dir_speed(tokens)
    assert_equals(decoder.wind_dir_speed, '18004KT')

  def test_process_winds_with_gusts(self):
    decoder = MetarDecoder()
    tokens = '21016G24KT 10SM'.split()
    res = decoder.process_wind_dir_speed(tokens)
    assert_equals(decoder.wind_dir_speed, '21016G24KT')

  def test_process_winds_variable(self):
    decoder = MetarDecoder()
    tokens = '18015KT 150V210 10SM'.split()
    # Make sure both the wind info and direction variation get picked up
    res = decoder.process_wind_dir_speed(tokens)
    res = decoder.process_wind_dir_variation(res)
    assert_equals(decoder.wind_dir_speed, '18015KT')
    assert_equals(decoder.wind_dir_variation, '150V210')

  def test_process_winds_variable_missing(self):
    ### If the variable winds section is missing we shouldn't set the
    ### MetarDecoder's wind_dir_variation field, or strip anything
    decoder = MetarDecoder()
    tokens = '18015KT 10SM'.split()
    # Include the wind_dir_speed processor for a sanity check
    res = decoder.process_wind_dir_speed(tokens)
    res = decoder.process_wind_dir_variation(res)
    assert_equals(decoder.wind_dir_speed, '18015KT')
    assert_equals(decoder.wind_dir_variation, '')
    assert_equals(res, ['10SM'])

  def test_process_visibility(self):
    decoder = MetarDecoder()
    tokens = '10SM R11/P6000FT'.split()
    res = decoder.process_visibility(tokens)
    assert_equals(decoder.vis, '10SM')
    assert_equals(res[0], 'R11/P6000FT')

  def test_process_visibility_missing(self):
    ### If the visibility field is missing, the MetarDecoder's 'vis' field
    ### should remain unset and nothing stripped from the METAR
    decoder = MetarDecoder()
    tokens = '21016G24KT R11/P6000FT'.split()
    res = decoder.process_visibility(tokens)
    assert_equals(decoder.vis, '')
    assert_equals(res, ['21016G24KT', 'R11/P6000FT'])

  def test_process_rvr(self):
    decoder = MetarDecoder()
    tokens = 'R11/P6000FT -RA BR'.split()
    res = decoder.process_rvr(tokens)
    assert_equals(decoder.rvr, 'R11/P6000FT')
    assert_equals(res, ['-RA', 'BR'])

  def test_process_rvr_missing(self):
    ### If the RVR is missing, the MetarDecoder's 'rvr' field should
    ### remain unset and nothing stripped from the METAR
    decoder = MetarDecoder()
    tokens = 'VRB005 -RA BR'.split()
    res = decoder.process_rvr(tokens)
    assert_equals(decoder.rvr, '')
    assert_equals(res, ['VRB005', '-RA', 'BR'])

  def test_process_rvr_missing_with_similar_wx_phenomena(self):
    ### The RVR field begins with 'R', but the following WX phenomena
    ### section can also start with 'R' in the case of moderate rain: 'RA'.
    ### This test ensures we don't mis-identify 'RA' as the RVR field.
    decoder = MetarDecoder()
    tokens = '18015KT RA'.split()
    res = decoder.process_wind_dir_speed(tokens)
    res = decoder.process_rvr(res)
    assert_equals(decoder.rvr, '')
    assert_equals(res, ['RA'])

  def test_process_wx_phenomena(self):
    decoder = MetarDecoder()
    tokens = '-RA BR BKN015 OVC025'.split()
    res = decoder.process_wx_phenomena(tokens)
    assert_equals(decoder.wx_phenomena, ['-RA', 'BR'])
    assert_equals(res, ['BKN015', 'OVC025'])

  def test_process_wx_phenomena_missing(self):
    decoder = MetarDecoder()
    tokens = 'FEW020 SCT150'.split()
    res = decoder.process_wx_phenomena(tokens)
    assert_equals(decoder.wx_phenomena, [])
    assert_equals(res, ['FEW020', 'SCT150'])

  def test_process_sky_condition(self):
    decoder = MetarDecoder()
    tokens = 'BKN015 OVC025 06/04'.split()
    res = decoder.process_sky_condition(tokens)
    assert_equals(decoder.sky_condition, ['BKN015', 'OVC025'])
    assert_equals(res, ['06/04'])

  def test_process_sky_condition_missing(self):
    decoder = MetarDecoder()
    tokens = '06/04 A2990'.split()
    res = decoder.process_sky_condition(tokens)
    assert_equals(decoder.sky_condition, [])
    assert_equals(res, ['06/04', 'A2990'])

  def test_process_tmp_dewpoint(self):
    decoder = MetarDecoder()
    tokens = '06/04 A2990'.split()
    res = decoder.process_temp_dewpoint(tokens)
    assert_equals(decoder.temp, '06')
    assert_equals(decoder.dewpoint, '04')
    assert_equals(res, ['A2990'])

  def test_process_temp_dewpoint_missing(self):
    decoder = MetarDecoder()
    tokens = 'A2990 RMK'.split()
    res = decoder.process_temp_dewpoint(tokens)
    assert_equals(decoder.temp, '')
    assert_equals(decoder.dewpoint, '')
    assert_equals(res, ['A2990', 'RMK'])

  def test_process_altimeter(self):
    decoder = MetarDecoder()
    tokens = 'A2990 RMK'.split()
    res = decoder.process_altimeter(tokens)
    assert_equals(decoder.altimeter, 'A2990')
    assert_equals(res, ['RMK'])

  def test_process_altimeter_missing(self):
    decoder = MetarDecoder()
    tokens = 'RMK TORNADO'.split()
    res = decoder.process_altimeter(tokens)
    assert_equals(decoder.altimeter, '')
    assert_equals(res, ['RMK', 'TORNADO'])

  @classmethod
  def teardown_class(cls):
    pass
