# -*- coding: utf-8 -*-

from nose import with_setup
from nose.tools import assert_equals
import json

from metars.workers.metar_decoder import MetarDecoder

class TestMetarController:

  DECODED_KEY = "decoded"

  @classmethod
  def setup_class(cls):
    pass

  # Tests get run from wxdecoder root directory
  def test_decode_metar(self):
    with open('metars/workers/tests/data/khio-encoded.json') as data:
      khio = json.load(data)
    decoder = MetarDecoder()
    decoder.decode_metar(khio["metar"])

  def test_decode_is_special_report(self):
    val = True
    decoder = MetarDecoder()
    decoder.decode_is_special_report(val)
    res = decoder.decoded_metar["is_special_report"][self.DECODED_KEY]
    assert_equals(res, True)

  def test_decode_is_not_special_report(self):
    val = False
    decoder = MetarDecoder()
    decoder.decode_is_special_report(val)
    res = decoder.decoded_metar["is_special_report"][self.DECODED_KEY]
    assert_equals(res, False)

  def test_decode_icao_id(self):
    val = "KPDX"
    decoder = MetarDecoder()
    decoder.decode_icao_id(val)
    res = decoder.decoded_metar["icao_id"][self.DECODED_KEY]
    assert_equals(res, "KPDX")

  def test_decode_obs_datetime(self):
    val = "290653Z"
    decoder = MetarDecoder()
    decoder.decode_obs_datetime(val)
    res_date = decoder.decoded_metar["obs_datetime"][self.DECODED_KEY]["date"]
    res_time = decoder.decoded_metar["obs_datetime"][self.DECODED_KEY]["time"]
    assert_equals(res_date, "29")
    assert_equals(res_time, "0653")

  def test_decode_is_automated(self):
    val = True
    decoder = MetarDecoder()
    decoder.decode_mod_auto(val)
    res = decoder.decoded_metar["mod_auto"][self.DECODED_KEY]
    assert_equals(res, True)

  def test_decode_is_not_automated(self):
    val = False
    decoder = MetarDecoder()
    decoder.decode_mod_auto(val)
    res = decoder.decoded_metar["mod_auto"][self.DECODED_KEY]
    assert_equals(res, False)

  def test_decode_wind_dir_speed_basic(self):
    val = "11013KT"
    decoder = MetarDecoder()
    decoder.decode_wind_dir_speed(val)
    res = decoder.decoded_metar["wind_dir_speed"][self.DECODED_KEY]
    assert_equals(res, "from 110 degrees, at 13 knots")

  def test_decode_wind_dir_speed_with_gusts(self):
    val = "18014G18KT"
    decoder = MetarDecoder()
    decoder.decode_wind_dir_speed(val)
    res = decoder.decoded_metar["wind_dir_speed"][self.DECODED_KEY]
    assert_equals(res, "from 180 degrees, at 14 knots gusting to 18 knots")

  def test_decode_wind_speed_calm(self):
    val = "00000KT"
    decoder = MetarDecoder()
    decoder.decode_wind_dir_speed(val)
    res = decoder.decoded_metar["wind_dir_speed"][self.DECODED_KEY]
    assert_equals(res, "calm winds")

  def test_decode_wind_single_knot_speed_isnt_pluralized(self):
    val = "02001KT"
    decoder = MetarDecoder()
    decoder.decode_wind_dir_speed(val)
    res = decoder.decoded_metar["wind_dir_speed"][self.DECODED_KEY]
    assert_equals(res, "from 020 degrees, at 1 knot")

  def test_decode_wind_light_variable(self):
    val = "VRB004KT"
    decoder = MetarDecoder()
    decoder.decode_wind_dir_speed(val)
    res = decoder.decoded_metar["wind_dir_speed"][self.DECODED_KEY]
    assert_equals(res, "variable, at 4 knots")

  def test_decode_wind_light_variable_single_knot_isnt_pluralized(self):
    val = "VRB001KT"
    decoder = MetarDecoder()
    decoder.decode_wind_dir_speed(val)
    res = decoder.decoded_metar["wind_dir_speed"][self.DECODED_KEY]
    assert_equals(res, "variable, at 1 knot")

  def test_decode_wind_variation(self):
    val = "180V250"
    decoder = MetarDecoder()
    decoder.decode_wind_dir_variation(val)
    res = decoder.decoded_metar["wind_dir_variation"][self.DECODED_KEY]
    assert_equals(res, "variable, from 180 degrees to 250 degrees")

  def test_decoded_wind_variation_missing(self):
    val = ""
    decoder = MetarDecoder()
    decoder.decode_wind_dir_variation(val)
    # The decoder should handle an empty wind variation, and the keys
    # should exist in the decoded metar with empty values.
    res = decoder.decoded_metar["wind_dir_variation"][self.DECODED_KEY]
    assert_equals(res, "")

  def test_decode_vis(self):
    val = "10SM"
    decoder = MetarDecoder()
    decoder.decode_vis(val)
    res = decoder.decoded_metar["vis"][self.DECODED_KEY]
    assert_equals(res, "10 statute miles")

  def test_decode_vis_with_fractional_part(self):
    val = "1 1/4SM"
    decoder = MetarDecoder()
    decoder.decode_vis(val)
    res = decoder.decoded_metar["vis"][self.DECODED_KEY]
    assert_equals(res, "1 1/4 statute miles")

  def test_decode_vis_less_than_quarter_mile(self):
    val = "M1/4SM"
    decoder = MetarDecoder()
    decoder.decode_vis(val)
    res = decoder.decoded_metar["vis"][self.DECODED_KEY]
    assert_equals(res, "less than 1/4 statute mile")

  def test_decode_vis_single_mile_isnt_pluralized(self):
    val = "1SM"
    decoder = MetarDecoder()
    decoder.decode_vis(val)
    res = decoder.decoded_metar["vis"][self.DECODED_KEY]
    assert_equals(res, "1 statute mile")

  def test_decode_rvr(self):
    val = "R06/2000FT"
    decoder = MetarDecoder()
    decoder.decode_rvr(val)
    res = decoder.decoded_metar["rvr"][self.DECODED_KEY]
    assert_equals(res, "2,000 feet (runway 06)")

  def test_decode_rvr_with_parallel_runways(self):
    val = "R32C/3500FT"
    decoder = MetarDecoder()
    decoder.decode_rvr(val)
    res = decoder.decoded_metar["rvr"][self.DECODED_KEY]
    assert_equals(res, "3,500 feet (runway 32C)")

  def test_decode_rvr_with_less_than_modifier(self):
    val = "R10/M4000FT"
    decoder = MetarDecoder()
    decoder.decode_rvr(val)
    res = decoder.decoded_metar["rvr"][self.DECODED_KEY]
    assert_equals(res, "less than 4,000 feet (runway 10)")

  def test_decode_rvr_with_more_than_modifier(self):
    val = "R36/P6000FT"
    decoder = MetarDecoder()
    decoder.decode_rvr(val)
    res = decoder.decoded_metar["rvr"][self.DECODED_KEY]
    assert_equals(res, "more than 6,000 feet (runway 36)")

  def test_decode_rvr_with_variation(self):
    val = "R25R/2000V4000FT"
    decoder = MetarDecoder()
    decoder.decode_rvr(val)
    res = decoder.decoded_metar["rvr"][self.DECODED_KEY]
    assert_equals(res, "variable, from 2,000 to 4,000 feet " \
      "(runway 25R)")

  def test_decode_rvr_with_downward_trend(self):
    val = "R36/4000FT/D"
    decoder = MetarDecoder()
    decoder.decode_rvr(val)
    res = decoder.decoded_metar["rvr"][self.DECODED_KEY]
    assert_equals(res, "4,000 feet, trending downward (runway 36)")

  def test_decode_rvr_with_upward_trend(self):
    val = "R02C/1500FT/U"
    decoder = MetarDecoder()
    decoder.decode_rvr(val)
    res = decoder.decoded_metar["rvr"][self.DECODED_KEY]
    assert_equals(res, "1,500 feet, trending upward (runway 02C)")

  def test_decode_rvr_with_no_change(self):
    val = "R20/5500FT/N"
    decoder = MetarDecoder()
    decoder.decode_rvr(val)
    res = decoder.decoded_metar["rvr"][self.DECODED_KEY]
    assert_equals(res, "5,500 feet, no change (runway 20)")


  def test_decode_wx_phenomena_basic(self):
    val = ["SHRA"]
    decoder = MetarDecoder()
    decoder.decode_wx_phenomena(val)
    res = decoder.decoded_metar["wx_phenomena"][self.DECODED_KEY]
    assert_equals(res, ["moderate showers of rain"])

  def test_decode_wx_phenomena_in_the_vicinity(self):
    val = ["VCFG"]
    decoder = MetarDecoder()
    decoder.decode_wx_phenomena(val)
    res = decoder.decoded_metar["wx_phenomena"][self.DECODED_KEY]
    assert_equals(res, ["fog in the vicinity"])

  def test_decode_wx_phenomena_modifiers(self):
    decoder = MetarDecoder()
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
    decoder = MetarDecoder()
    decoder.decode_wx_phenomena(val)
    res = decoder.decoded_metar["wx_phenomena"][self.DECODED_KEY]
    assert_equals(res, ["funnel cloud (tornado or waterspout)"])

  def test_decode_wx_phenomena_multiple_values(self):
    val = ["-SHRA", "+BR"]
    decoder = MetarDecoder()
    decoder.decode_wx_phenomena(val)
    res = decoder.decoded_metar["wx_phenomena"][self.DECODED_KEY]
    assert_equals(res, ["light showers of rain", "heavy mist"])

  def test_decode_sky_condition_basic(self):
    val = ["FEW020"]
    decoder = MetarDecoder()
    decoder.decode_sky_condition(val)
    res = decoder.decoded_metar["sky_condition"][self.DECODED_KEY]
    assert_equals(res, ["few clouds at 2,000 feet"])

  def test_decode_sky_condition_sky_clear(self):
    val = ["SKC"]
    decoder = MetarDecoder()
    decoder.decode_sky_condition(val)
    res = decoder.decoded_metar["sky_condition"][self.DECODED_KEY]
    assert_equals(res, ["sky clear"])

  def test_decode_sky_condition_sky_clear_automated(self):
    val = ["CLR"]
    decoder = MetarDecoder()
    decoder.decode_sky_condition(val)
    res = decoder.decoded_metar["sky_condition"][self.DECODED_KEY]
    assert_equals(res, ["no clouds below 12,000 feet"])

  def test_decode_sky_condition_vertical_visibility(self):
    val = ["VV048"]
    decoder = MetarDecoder()
    decoder.decode_sky_condition(val)
    res = decoder.decoded_metar["sky_condition"][self.DECODED_KEY]
    assert_equals(res, ["vertical visibility (indefinite ceiling) at 4,800 feet"])

  def test_decode_sky_condition_cumulonimbus(self):
    val = ["SCT085CB"]
    decoder = MetarDecoder()
    decoder.decode_sky_condition(val)
    res = decoder.decoded_metar["sky_condition"][self.DECODED_KEY]
    assert_equals(res, ["scattered clouds at 8,500 feet (cumulonimbus)"])

  def test_decode_sky_condition_towering_cumulus(self):
    val = ["OVC030TCU"]
    decoder = MetarDecoder()
    decoder.decode_sky_condition(val)
    res = decoder.decoded_metar["sky_condition"][self.DECODED_KEY]
    assert_equals(res, ["overcast at 3,000 feet (towering cumulus)"])

  def test_decode_sky_condition_altitude_below_station(self):
    val = ["SCT///"]
    decoder = MetarDecoder()
    decoder.decode_sky_condition(val)
    res = decoder.decoded_metar["sky_condition"][self.DECODED_KEY]
    assert_equals(res, ["scattered clouds below reporting station elevation"])

  def test_decode_sky_condition_multiple_layers(self):
    val = ["SCT///", "FEW032", "OVC100TCU"]
    decoder = MetarDecoder()
    decoder.decode_sky_condition(val)
    res = decoder.decoded_metar["sky_condition"][self.DECODED_KEY]
    assert_equals(res, ["scattered clouds below reporting station elevation",
                        "few clouds at 3,200 feet",
                        "overcast at 10,000 feet (towering cumulus)"])

  def test_decode_temp(self):
    val = "10"
    decoder = MetarDecoder()
    decoder.decode_temp(val)
    res = decoder.decoded_metar["temp"][self.DECODED_KEY]
    degree_sign = u'\N{DEGREE SIGN}'
    assert_equals(res, "10%sC" % degree_sign)

  def test_decode_temp_missing(self):
    val = ""
    decoder = MetarDecoder()
    decoder.decode_temp(val)
    res = decoder.decoded_metar["temp"][self.DECODED_KEY]
    assert_equals(res, "(missing)")

  def test_decode_temp_negative(self):
    val = "M04"
    decoder = MetarDecoder()
    decoder.decode_temp(val)
    res = decoder.decoded_metar["temp"][self.DECODED_KEY]
    degree_sign = u'\N{DEGREE SIGN}'
    assert_equals(res, "minus 4%sC" % degree_sign)

  def test_decode_temp_single_digit_degree_gets_leading_zero_stripped(self):
    val = "09"
    decoder = MetarDecoder()
    decoder.decode_temp(val)
    res = decoder.decoded_metar["temp"][self.DECODED_KEY]
    degree_sign = u'\N{DEGREE SIGN}'
    assert_equals(res, "9%sC" % degree_sign)

  def test_decode_dewpoint(self):
    val = "10"
    decoder = MetarDecoder()
    decoder.decode_dewpoint(val)
    res = decoder.decoded_metar["dewpoint"][self.DECODED_KEY]
    degree_sign = u'\N{DEGREE SIGN}'
    assert_equals(res, "10%sC" % degree_sign)

  def test_decode_dewpoint_missing(self):
    val = ""
    decoder = MetarDecoder()
    decoder.decode_dewpoint(val)
    res = decoder.decoded_metar["dewpoint"][self.DECODED_KEY]
    assert_equals(res, "(missing)")

  def test_decode_dewpoint_negative(self):
    val = "M04"
    decoder = MetarDecoder()
    decoder.decode_dewpoint(val)
    res = decoder.decoded_metar["dewpoint"][self.DECODED_KEY]
    degree_sign = u'\N{DEGREE SIGN}'
    assert_equals(res, "minus 4%sC" % degree_sign)

  def test_decode_dewpoint_single_digit_degree_gets_leading_zero_stripped(self):
    val = "09"
    decoder = MetarDecoder()
    decoder.decode_dewpoint(val)
    res = decoder.decoded_metar["dewpoint"][self.DECODED_KEY]
    degree_sign = u'\N{DEGREE SIGN}'
    assert_equals(res, "9%sC" % degree_sign)

  def test_decode_altimeter(self):
    val = "2992"
    decoder = MetarDecoder()
    decoder.decode_altimeter(val)
    res = decoder.decoded_metar["altimeter"][self.DECODED_KEY]
    assert_equals(res, "29.92\"Hg")

  def test_decode_stn_type_ao1(self):
    val = "AO1"
    decoder = MetarDecoder()
    decoder.decode_stn_type(val)
    res = decoder.decoded_metar["stn_type"][self.DECODED_KEY]
    assert_equals(res, "automated station with no precipitation sensor")

  def test_decode_stn_type_ao2(self):
    val = "AO2"
    decoder = MetarDecoder()
    decoder.decode_stn_type(val)
    res = decoder.decoded_metar["stn_type"][self.DECODED_KEY]
    assert_equals(res, "automated station with precipitation sensor")

  def test_decode_stn_type_unknown(self):
    val = "thesearenotthestationsyourelookingfor"
    decoder = MetarDecoder()
    decoder.decode_stn_type(val)
    res = decoder.decoded_metar["stn_type"][self.DECODED_KEY]
    assert_equals(res, "unknown station type '" + val + "'")

  # NB. SLP values are kind of funky, for more info see metar_decoder.py
  def test_decode_sea_level_pressure_greater_than_50(self):
    val = "SLP834"
    decoder = MetarDecoder()
    decoder.decode_sea_level_pressure(val)
    res = decoder.decoded_metar["sea_level_pressure"][self.DECODED_KEY]
    assert_equals(res, "sea level pressure is 983.4 hPa")

  def test_decode_sea_level_pressure_less_than_50(self):
    val = "SLP196"
    decoder = MetarDecoder()
    decoder.decode_sea_level_pressure(val)
    res = decoder.decoded_metar["sea_level_pressure"][self.DECODED_KEY]
    assert_equals(res, "sea level pressure is 1,019.6 hPa")

  def test_decode_sea_level_pressure_is_50(self):
    # SLP >= 50 should have 900 hPa added
    val = "SLP500"
    decoder = MetarDecoder()
    decoder.decode_sea_level_pressure(val)
    res = decoder.decoded_metar["sea_level_pressure"][self.DECODED_KEY]
    assert_equals(res, "sea level pressure is 950.0 hPa")

  def test_decode_sea_level_pressure_less_49_point_9(self):
    # Edge case for SLP < 50 should have 1,000 hPa added
    val = "SLP499"
    decoder = MetarDecoder()
    decoder.decode_sea_level_pressure(val)
    res = decoder.decoded_metar["sea_level_pressure"][self.DECODED_KEY]
    assert_equals(res, "sea level pressure is 1,049.9 hPa")

  def test_decode_sea_level_pressure_is_garbage(self):
    val = "noSLPforyou"
    decoder = MetarDecoder()
    decoder.decode_sea_level_pressure(val)
    res = decoder.decoded_metar["sea_level_pressure"][self.DECODED_KEY]
    assert_equals(res, "")

  def test_decode_no_sea_level_pressure(self):
    val = "SLPNO"
    decoder = MetarDecoder()
    decoder.decode_sea_level_pressure(val)
    res = decoder.decoded_metar["sea_level_pressure"][self.DECODED_KEY]
    assert_equals(res, "sea level pressure unavailable")

  def test_decode_hourly_temp_dewpoint(self):
    val = "T00560050"
    decoder = MetarDecoder()
    decoder.decode_hourly_temp_dewpoint(val)
    res = decoder.decoded_metar["hourly_temp_dewpoint"][self.DECODED_KEY]
    assert_equals(res, [5.6, 5.0])

  def test_decode_hourly_temp_dewpoint_both_negative(self):
    val = "T11631172"
    decoder = MetarDecoder()
    decoder.decode_hourly_temp_dewpoint(val)
    res = decoder.decoded_metar["hourly_temp_dewpoint"][self.DECODED_KEY]
    assert_equals(res, [-16.3, -17.2])

  def test_decode_hourly_temp_dewpoint_temp_neg_dewpoint_pos(self):
    val = "T10230012"
    decoder = MetarDecoder()
    decoder.decode_hourly_temp_dewpoint(val)
    res = decoder.decoded_metar["hourly_temp_dewpoint"][self.DECODED_KEY]
    assert_equals(res, [-2.3, 1.2])

  def test_decode_hourly_temp_dewpoint_temp_pos_dewpoint_neg(self):
    val = "T00801010"
    decoder = MetarDecoder()
    decoder.decode_hourly_temp_dewpoint(val)
    res = decoder.decoded_metar["hourly_temp_dewpoint"][self.DECODED_KEY]
    assert_equals(res, [8.0, -1.0])

  def test_decode_hourly_temp_dewpoint_both_zero(self):
    val = "T00000000"
    decoder = MetarDecoder()
    decoder.decode_hourly_temp_dewpoint(val)
    res = decoder.decoded_metar["hourly_temp_dewpoint"][self.DECODED_KEY]
    assert_equals(res, [0.0, 0.0])

  def test_decode_hourly_temp_dewpoint_both_neg_eleven_point_one(self):
    val = "T11111111"
    decoder = MetarDecoder()
    decoder.decode_hourly_temp_dewpoint(val)
    res = decoder.decoded_metar["hourly_temp_dewpoint"][self.DECODED_KEY]
    assert_equals(res, [-11.1, -11.1])
