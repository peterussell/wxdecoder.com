import json

class MetarDecoder:

  def decode_metar(self, json_metar):
    self.decode_is_special_report(json_metar["is_special_report"])
    self.decode_icao_id(json_metar["icao_id"])
    self.decode_obs_datetime(json_metar["obs_datetime"])
    self.decode_mod_auto(json_metar["mod_auto"])
    self.decode_wind_dir_speed(json_metar["wind_dir_speed"])
    self.decode_wind_dir_variation(json_metar["wind_dir_variation"])
    self.decode_vis(json_metar["vis"])
    self.decode_rvr(json_metar["rvr"])
    self.decode_wx_phenomena(json_metar["wx_phenomena"])
    self.decode_sky_condition(json_metar["sky_condition"])
    self.decode_temp(json_metar["temp"])
    self.decode_dewpoint(json_metar["dewpoint"])
    self.decode_altimeter(json_metar["altimeter"])
    self.decode_remarks(json_metar["remarks"])
    self.decode_tornadic_activity(json_metar["tornadic_activity"])
    self.decode_stn_type(json_metar["stn_type"])
    self.decode_peak_wind(json_metar["peak_wind"])
    self.decode_wind_shift(json_metar["wind_shift"])
    self.decode_variable_vis(json_metar["variable_vis"])
    self.decode_vis_second_loc(json_metar["vis_second_loc"])
    self.decode_lightning(json_metar["lightning"])
    self.decode_precip_ts(json_metar["precip_ts"])
    self.decode_virga(json_metar["virga"])
    self.decode_variable_ceiling(json_metar["variable_ceiling"])
    self.decode_ceiling_second_loc(json_metar["ceiling_second_loc"])
    self.decode_pressure_rise_fall_rapid(json_metar["pressure_rise_fall_rapid"])
    self.decode_sea_level_pressure(json_metar["sea_level_pressure"])
    self.decode_hourly_precip(json_metar["hourly_precip"])
    self.decode_three_six_hour_precip(json_metar["three_six_hour_precip"])
    self.decode_twenty_four_hour_precip(json_metar["twenty_four_hour_precip"])
    self.decode_pressure_tendency(json_metar["pressure_tendency"])
    self.decode_sensor_status(json_metar["sensor_status"])

    # tmp
    return json_metar

  def decode_is_special_report(self, val):
    key = "is_special_report"
    self.copy_orig_value(key, val)
    self.decoded_metar[key]["decoded"] = val

  def decode_icao_id(self, val):
    key = "icao_id"
    self.copy_orig_value(key, val)
    self.decoded_metar[key]["decoded"] = val

  def decode_obs_datetime(self, val):
    key = "obs_datetime"
    self.copy_orig_value(key, val)
    self.decoded_metar[key]["decoded"]["date"] = val[:2]
    self.decoded_metar[key]["decoded"]["time"] = val[2:-1]

  def decode_mod_auto(self, val):
    key = "mod_auto"
    self.copy_orig_value(key, val)
    self.decoded_metar[key]["decoded"] = val

  def decode_wind_dir_speed(self, val):
    key = "wind_dir_speed"
    self.copy_orig_value(key, val)

    # Handle light and variable winds (< 7KTS)
    if val.startswith("VRB"):
      kt_index = val.find("KT")
      speed = val[4:kt_index].lstrip("0")
      speed_unit = self.get_knot_or_knots(speed)
      self.decoded_metar[key]["decoded"] = \
        "variable, at %s %s" % (speed, speed_unit)
      return

    # Wind direction is always 3 characters
    direction = val[:3]

    kt_index = val.find("KT")
    gust_index = val.find("G")

    # Keep going until we get to 'G' or 'KT'
    has_gusts = gust_index != -1
    if has_gusts:
      speed = val[3:gust_index]
      gust = val[gust_index+1:kt_index]
    else:
      speed = val[3:kt_index]
      gust = ""

    # Strip any leading 0s on the wind speed
    speed = speed.lstrip("0")
    speed_unit = self.get_knot_or_knots(speed)

    # Assemble the output
    res = "from %s degrees, at %s %s" % (direction, speed, speed_unit)
    if has_gusts:
      res += " gusting to %s knots" % gust

    self.decoded_metar[key]["decoded"] = res

  def decode_wind_dir_variation(self, val):
    pass

  def decode_vis(self, val):
    pass

  def decode_rvr(self, val):
    pass

  def decode_wx_phenomena(self, val):
    pass

  def decode_sky_condition(self, val):
    pass

  def decode_temp(self, val):
    pass

  def decode_dewpoint(self, val):
    pass

  def decode_altimeter(self, val):
    pass

  def decode_remarks(self, val):
    pass

  def decode_tornadic_activity(self, val):
    pass

  def decode_stn_type(self, val):
    pass

  def decode_peak_wind(self, val):
    pass

  def decode_wind_shift(self, val):
    pass

  def decode_variable_vis(self, val):
    pass

  def decode_vis_second_loc(self, val):
    pass

  def decode_lightning(self, val):
    pass

  def decode_precip_ts(self, val):
    pass

  def decode_virga(self, val):
    pass

  def decode_variable_ceiling(self, val):
    pass

  def decode_ceiling_second_loc(self, val):
    pass

  def decode_pressure_rise_fall_rapid(self, val):
    pass

  def decode_sea_level_pressure(self, val):
    pass

  def decode_hourly_precip(self, val):
    pass

  def decode_three_six_hour_precip(self, val):
    pass

  def decode_twenty_four_hour_precip(self, val):
    pass

  def decode_pressure_tendency(self, val):
    pass

  def decode_sensor_status(self, val):
    pass

  def decode_maint_reqd(self, val):
    pass

  ## Helpers
  def copy_orig_value(self, key, value):
    self.decoded_metar[key]["orig"] = value

  def get_knot_or_knots(self, num_knots):
    try:
      val = int(num_knots)
      if val == 1:
        return "knot"
      else:
        return "knots"
    except ValueError:
      return "knots"


  def __init__(self):
    # Load defaults
    with open('metar-decoded-defaults.json') as decoded_metar_file:
      contents = json.load(decoded_metar_file)
      self.decoded_metar = contents["metar"]
