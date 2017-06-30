# -*- coding: utf-8 -*-

from nose import with_setup
from nose.tools import assert_equals
import json

from metars.workers.decoders.nz import MetarDecoderNZ

class TestMetarDecoderNZ:

  DECODED_KEY = "decoded"

  @classmethod
  def setup_class(self):
    pass

  def test_decode_is_special_report(self):
    val = True
    decoder = MetarDecoderNZ()
    decoder.decode_is_special_report(val)
    res = decoder.decoded_metar["is_special_report"][self.DECODED_KEY]
    assert_equals(res, True)

  def test_decode_is_not_special_report(self):
    val = False
    decoder = MetarDecoderNZ()
    decoder.decode_is_special_report(val)
    res = decoder.decoded_metar["is_special_report"][self.DECODED_KEY]
    assert_equals(res, False)

  def test_decode_icao_id(self):
    val = "NZCH"
    decoder = MetarDecoderNZ()
    decoder.decode_icao_id(val)
    res = decoder.decoded_metar["icao_id"][self.DECODED_KEY]
    assert_equals(res, "NZCH")

  def test_decode_obs_datetime(self):
    val = "301900Z"
    decoder = MetarDecoderNZ()
    decoder.decode_obs_datetime(val)
    res_date = decoder.decoded_metar["obs_datetime"][self.DECODED_KEY]["date"]
    res_time = decoder.decoded_metar["obs_datetime"][self.DECODED_KEY]["time"]
    assert_equals(res_date, "30")
    assert_equals(res_time, "1900")

  def test_decode_is_automated(self):
    val = True
    decoder = MetarDecoderNZ()
    decoder.decode_mod_auto(val)
    res = decoder.decoded_metar["mod_auto"][self.DECODED_KEY]
    assert_equals(res, True)

  def test_decode_is_not_automated(self):
    val = False
    decoder = MetarDecoderNZ()
    decoder.decode_mod_auto(val)
    res = decoder.decoded_metar["mod_auto"][self.DECODED_KEY]
    assert_equals(res, False)

  def test_decode_wind_dir_speed_basic(self):
    val = "04003KT"
    decoder = MetarDecoderNZ()
    decoder.decode_wind_dir_speed(val)
    res = decoder.decoded_metar["wind_dir_speed"][self.DECODED_KEY]
    assert_equals(res, "from 040 degrees, at 3 knots")

  def test_decode_wind_dir_speed_with_gusts(self):
    val = "03019G29KT"
    decoder = MetarDecoderNZ()
    decoder.decode_wind_dir_speed(val)
    res = decoder.decoded_metar["wind_dir_speed"][self.DECODED_KEY]
    assert_equals(res, "from 030 degrees, at 19 knots gusting to 29 knots")

  def test_decode_wind_speed_calm(self):
    val = "00000KT"
    decoder = MetarDecoderNZ()
    decoder.decode_wind_dir_speed(val)
    res = decoder.decoded_metar["wind_dir_speed"][self.DECODED_KEY]
    assert_equals(res, "calm winds")

  def test_decode_wind_single_knot_speed_isnt_pluralized(self):
    val = "02001KT"
    decoder = MetarDecoderNZ()
    decoder.decode_wind_dir_speed(val)
    res = decoder.decoded_metar["wind_dir_speed"][self.DECODED_KEY]
    assert_equals(res, "from 020 degrees, at 1 knot")

  def test_decode_wind_light_variable(self):
    val = "VRB002KT"
    decoder = MetarDecoderNZ()
    decoder.decode_wind_dir_speed(val)
    res = decoder.decoded_metar["wind_dir_speed"][self.DECODED_KEY]
    assert_equals(res, "variable, at 2 knots")

  def test_decode_wind_light_variable_single_knot_isnt_pluralized(self):
    val = "VRB001KT"
    decoder = MetarDecoderNZ()
    decoder.decode_wind_dir_speed(val)
    res = decoder.decoded_metar["wind_dir_speed"][self.DECODED_KEY]
    assert_equals(res, "variable, at 1 knot")

  def test_decode_wind_variation(self):
    val = "260V330"
    decoder = MetarDecoderNZ()
    decoder.decode_wind_dir_variation(val)
    res = decoder.decoded_metar["wind_dir_variation"][self.DECODED_KEY]
    assert_equals(res, "variable, from 260 degrees to 330 degrees")

  def test_decoded_wind_variation_missing(self):
    val = ""
    decoder = MetarDecoderNZ()
    decoder.decode_wind_dir_variation(val)
    # The decoder should handle an empty wind variation, and the keys
    # should exist in the decoded metar with empty values.
    res = decoder.decoded_metar["wind_dir_variation"][self.DECODED_KEY]
    assert_equals(res, "")

  def test_decode_vis_less_than_10km(self):
    val = "7000"
    decoder = MetarDecoderNZ()
    decoder.decode_vis(val)
    res = decoder.decoded_metar["vis"][self.DECODED_KEY]
    assert_equals(res, "7,000 metres")

  def test_decode_vis_kilometres(self):
    val = "29KM"
    decoder = MetarDecoderNZ()
    decoder.decode_vis(val)
    res = decoder.decoded_metar["vis"][self.DECODED_KEY]
    assert_equals(res, "29 kilometres")

  def test_decode_vis_9999(self):
    val = "9999"
    decoder = MetarDecoderNZ()
    decoder.decode_vis(val)
    res = decoder.decoded_metar["vis"][self.DECODED_KEY]
    assert_equals(res, "10 kilometres or more")

  def test_decode_vis_CAVOK(self):
    val = "CAVOK"
    decoder = MetarDecoderNZ()
    decoder.decode_vis(val)
    res = decoder.decoded_metar["vis"][self.DECODED_KEY]
    assert_equals(res, "10 kilometres or more (Ceiling And Visibility OK)")

  def test_decode_vis_not_reported(self):
    val = "////"
    decoder = MetarDecoderNZ()
    decoder.decode_vis(val)
    res = decoder.decoded_metar["vis"][self.DECODED_KEY]
    assert_equals(res, "not reported (possibly due to a faulty sensor)")

  def test_decode_vis_single_km_isnt_pluralized(self):
    val = "1KM"
    decoder = MetarDecoderNZ()
    decoder.decode_vis(val)
    res = decoder.decoded_metar["vis"][self.DECODED_KEY]
    assert_equals(res, "1 kilometre")

  def test_decode_rvr(self):
    val = "R30/0500"
    decoder = MetarDecoderNZ()
    decoder.decode_rvr(val)
    res = decoder.decoded_metar["rvr"][self.DECODED_KEY]
    assert_equals(res, "500 metres (runway 30)")

  def test_decode_rvr_with_parallel_runways(self):
    val = "R23L/1400"
    decoder = MetarDecoderNZ()
    decoder.decode_rvr(val)
    res = decoder.decoded_metar["rvr"][self.DECODED_KEY]
    assert_equals(res, "1,400 metres (runway 23L)")

  def test_decode_rvr_with_less_than_modifier(self):
    val = "R10/M0050"
    decoder = MetarDecoderNZ()
    decoder.decode_rvr(val)
    res = decoder.decoded_metar["rvr"][self.DECODED_KEY]
    assert_equals(res, "less than 50 metres (runway 10)")

  def test_decode_rvr_with_more_than_modifier(self):
    val = "R36/P2000"
    decoder = MetarDecoderNZ()
    decoder.decode_rvr(val)
    res = decoder.decoded_metar["rvr"][self.DECODED_KEY]
    assert_equals(res, "more than 2,000 metres (runway 36)")

  def test_decode_rvr_with_downward_trend(self):
    val = "R36/0500D"
    decoder = MetarDecoderNZ()
    decoder.decode_rvr(val)
    res = decoder.decoded_metar["rvr"][self.DECODED_KEY]
    assert_equals(res, "500 metres, trending downward (runway 36)")

  def test_decode_rvr_with_upward_trend(self):
    val = "R02C/0200U"
    decoder = MetarDecoderNZ()
    decoder.decode_rvr(val)
    res = decoder.decoded_metar["rvr"][self.DECODED_KEY]
    assert_equals(res, "200 metres, trending upward (runway 02C)")

  def test_decode_rvr_with_no_change(self):
    val = "R20/1200N"
    decoder = MetarDecoderNZ()
    decoder.decode_rvr(val)
    res = decoder.decoded_metar["rvr"][self.DECODED_KEY]
    assert_equals(res, "1,200 metres, no change (runway 20)")

  def test_decode_wx_phenomena_basic(self):
    val = ["SHRA"]
    decoder = MetarDecoderNZ()
    decoder.decode_wx_phenomena(val)
    res = decoder.decoded_metar["wx_phenomena"][self.DECODED_KEY]
    assert_equals(res, ["moderate showers of rain"])

  def test_decode_wx_phenomena_sensor_inop(self):
    val = "//"
    decoder = MetarDecoderNZ()
    decoder.decode_wx_phenomena(val)
    res = decoder.decoded_metar["wx_phenomena"][self.DECODED_KEY]
    assert_equals(res, "none reported, sensor temporarily inoperative")

  def test_decode_wx_phenomena_in_the_vicinity(self):
    val = ["VCFG"]
    decoder = MetarDecoderNZ()
    decoder.decode_wx_phenomena(val)
    res = decoder.decoded_metar["wx_phenomena"][self.DECODED_KEY]
    assert_equals(res, ["fog in the vicinity"])

  def test_decode_wx_phenomena_modifiers(self):
    decoder = MetarDecoderNZ()
    # Light
    val = ["-PY"]
    decoder.decode_wx_phenomena(val)
    res = decoder.decoded_metar["wx_phenomena"][self.DECODED_KEY]
    assert_equals(res, ["light spray"])
    # Moderate
    val = ["PY"]
    decoder.decode_wx_phenomena(val)
    res = decoder.decoded_metar["wx_phenomena"][self.DECODED_KEY]
    assert_equals(res, ["moderate spray"])
    # Heavy
    val = ["+PY"]
    decoder.decode_wx_phenomena(val)
    res = decoder.decoded_metar["wx_phenomena"][self.DECODED_KEY]
    assert_equals(res, ["heavy spray"])

  def test_decode_wx_phenomena_tornado_waterspout_special_case(self):
    # +FC is a special case for tornadoes and waterspouts - the
    # modifier '+' should be ignored.
    val = ["+FC"]
    decoder = MetarDecoderNZ()
    decoder.decode_wx_phenomena(val)
    res = decoder.decoded_metar["wx_phenomena"][self.DECODED_KEY]
    assert_equals(res, ["funnel cloud (tornado or waterspout)"])

  def test_decode_wx_phenomena_multiple_values(self):
    val = ["-SHRA", "+BR"]
    decoder = MetarDecoderNZ()
    decoder.decode_wx_phenomena(val)
    res = decoder.decoded_metar["wx_phenomena"][self.DECODED_KEY]
    assert_equals(res, ["light showers of rain", "heavy mist"])

  def test_decode_sky_condition_basic(self):
    val = ["FEW020"]
    decoder = MetarDecoderNZ()
    decoder.decode_sky_condition(val)
    res = decoder.decoded_metar["sky_condition"][self.DECODED_KEY]
    assert_equals(res, ["few clouds at 2,000 feet"])

  def test_decode_sky_condition_sky_clear(self):
    val = ["SKC"]
    decoder = MetarDecoderNZ()
    decoder.decode_sky_condition(val)
    res = decoder.decoded_metar["sky_condition"][self.DECODED_KEY]
    assert_equals(res, ["sky clear"])

  # NCD means No Cloud Detected:
  #  -> below 10,000' at NZAA, NZWN, and NZCH
  #  -> at any altitude at all other domestic aerodromes
  def test_decode_sky_condition_no_cloud_detected_nzaa_nzwn_nzch(self):
    val = ["NCD"]
    decoder = MetarDecoderNZ()
    # NZAA
    decoder.decoded_metar["icao_id"][self.DECODED_KEY] = "NZAA"
    decoder.decode_sky_condition(val)
    res = decoder.decoded_metar["sky_condition"][self.DECODED_KEY]
    assert_equals(res, ["no cloud detected below 10,000 feet"])
    # NZAA
    decoder.decoded_metar["icao_id"][self.DECODED_KEY] = "NZWN"
    decoder.decode_sky_condition(val)
    res = decoder.decoded_metar["sky_condition"][self.DECODED_KEY]
    assert_equals(res, ["no cloud detected below 10,000 feet"])
    # NZAA
    decoder.decoded_metar["icao_id"][self.DECODED_KEY] = "NZCH"
    decoder.decode_sky_condition(val)
    res = decoder.decoded_metar["sky_condition"][self.DECODED_KEY]
    assert_equals(res, ["no cloud detected below 10,000 feet"])

  def test_decode_sky_condition_no_cloud_detected_other_aerodromes(self):
    val = ["NCD"]
    decoder = MetarDecoderNZ()
    decoder.decode_sky_condition(val)
    res = decoder.decoded_metar["sky_condition"][self.DECODED_KEY]
    assert_equals(res, ["no cloud detected"])

  def test_decode_sky_condition_sky_clear_automated(self):
    val = ["CLR"]
    decoder = MetarDecoderNZ()
    decoder.decode_sky_condition(val)
    res = decoder.decoded_metar["sky_condition"][self.DECODED_KEY]
    assert_equals(res, ["no clouds below 12,000 feet"])

  def test_decode_sky_condition_sensor_inop(self):
    val = ["/////////"]
    decoder = MetarDecoderNZ()
    decoder.decode_sky_condition(val)
    res = decoder.decoded_metar["sky_condition"][self.DECODED_KEY]
    assert_equals(res, ["not reported (possibly due to a faulty sensor)"])

  def test_decode_sky_condition_sensor_inop(self):
    val = ["VV///"]
    decoder = MetarDecoderNZ()
    decoder.decode_sky_condition(val)
    res = decoder.decoded_metar["sky_condition"][self.DECODED_KEY]
    assert_equals(res, ["vertical visibility unavailable"])

  def test_decode_sky_condition_vertical_visibility(self):
    val = ["VV048"]
    decoder = MetarDecoderNZ()
    decoder.decode_sky_condition(val)
    res = decoder.decoded_metar["sky_condition"][self.DECODED_KEY]
    assert_equals(res, ["vertical visibility (indefinite ceiling) at 4,800 feet"])

  def test_decode_sky_condition_vertical_visibility(self):
    val = ["OVC048///"]
    decoder = MetarDecoderNZ()
    decoder.decode_sky_condition(val)
    res = decoder.decoded_metar["sky_condition"][self.DECODED_KEY]
    assert_equals(res, ["overcast at 4,800 feet (unable to determine cloud type)"])

  def test_decode_sky_condition_cumulonimbus(self):
    val = ["SCT085CB"]
    decoder = MetarDecoderNZ()
    decoder.decode_sky_condition(val)
    res = decoder.decoded_metar["sky_condition"][self.DECODED_KEY]
    assert_equals(res, ["scattered clouds at 8,500 feet (cumulonimbus)"])

  def test_decode_sky_condition_towering_cumulus(self):
    val = ["OVC030TCU"]
    decoder = MetarDecoderNZ()
    decoder.decode_sky_condition(val)
    res = decoder.decoded_metar["sky_condition"][self.DECODED_KEY]
    assert_equals(res, ["overcast at 3,000 feet (towering cumulus)"])

  def test_decode_sky_condition_multiple_layers(self):
    val = ["SCT016///", "BKN085///", "OVC100TCU"]
    decoder = MetarDecoderNZ()
    decoder.decode_sky_condition(val)
    res = decoder.decoded_metar["sky_condition"][self.DECODED_KEY]
    assert_equals(res, ["scattered clouds at 1,600 feet (unable to determine " \
                        "cloud type)",
                        "broken clouds at 8,500 feet (unable to determine " \
                        "cloud type)",
                        "overcast at 10,000 feet (towering cumulus)"])

  def test_decode_temp(self):
    val = "10"
    decoder = MetarDecoderNZ()
    decoder.decode_temp(val)
    res = decoder.decoded_metar["temp"][self.DECODED_KEY]
    degree_sign = u'\N{DEGREE SIGN}'
    assert_equals(res, "10%sC" % degree_sign)

  def test_decode_temp_missing(self):
    val = ""
    decoder = MetarDecoderNZ()
    decoder.decode_temp(val)
    res = decoder.decoded_metar["temp"][self.DECODED_KEY]
    assert_equals(res, "(missing)")

  def test_decode_temp_negative(self):
    val = "M04"
    decoder = MetarDecoderNZ()
    decoder.decode_temp(val)
    res = decoder.decoded_metar["temp"][self.DECODED_KEY]
    degree_sign = u'\N{DEGREE SIGN}'
    assert_equals(res, "minus 4%sC" % degree_sign)

  def test_decode_temp_single_digit_degree_gets_leading_zero_stripped(self):
    val = "09"
    decoder = MetarDecoderNZ()
    decoder.decode_temp(val)
    res = decoder.decoded_metar["temp"][self.DECODED_KEY]
    degree_sign = u'\N{DEGREE SIGN}'
    assert_equals(res, "9%sC" % degree_sign)

  def test_decode_dewpoint(self):
    val = "10"
    decoder = MetarDecoderNZ()
    decoder.decode_dewpoint(val)
    res = decoder.decoded_metar["dewpoint"][self.DECODED_KEY]
    degree_sign = u'\N{DEGREE SIGN}'
    assert_equals(res, "10%sC" % degree_sign)

  def test_decode_dewpoint_missing(self):
    val = ""
    decoder = MetarDecoderNZ()
    decoder.decode_dewpoint(val)
    res = decoder.decoded_metar["dewpoint"][self.DECODED_KEY]
    assert_equals(res, "(missing)")

  def test_decode_dewpoint_negative(self):
    val = "M04"
    decoder = MetarDecoderNZ()
    decoder.decode_dewpoint(val)
    res = decoder.decoded_metar["dewpoint"][self.DECODED_KEY]
    degree_sign = u'\N{DEGREE SIGN}'
    assert_equals(res, "minus 4%sC" % degree_sign)

  def test_decode_dewpoint_single_digit_degree_gets_leading_zero_stripped(self):
    val = "09"
    decoder = MetarDecoderNZ()
    decoder.decode_dewpoint(val)
    res = decoder.decoded_metar["dewpoint"][self.DECODED_KEY]
    degree_sign = u'\N{DEGREE SIGN}'
    assert_equals(res, "9%sC" % degree_sign)

  def test_decode_altimeter(self):
    val = "Q1018"
    decoder = MetarDecoderNZ()
    decoder.decode_altimeter(val)
    res = decoder.decoded_metar["altimeter"][self.DECODED_KEY]
    assert_equals(res, "1,018 hPa")
