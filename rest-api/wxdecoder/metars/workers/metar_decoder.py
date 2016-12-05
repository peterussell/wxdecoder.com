class MetarDecoder:

  def decode_metar(self, json_metar):
    print ">>> Decoding metar: %s" % json_metar
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

  def decode_is_special_report(self, enc):
    pass

  def decode_icao_id(self, enc):
    pass

  def decode_obs_datetime(self, enc):
    pass

  def decode_mod_auto(self, enc):
    pass

  def decode_wind_dir_speed(self, enc):
    pass

  def decode_wind_dir_variation(self, enc):
    pass

  def decode_vis(self, enc):
    pass

  def decode_rvr(self, enc):
    pass

  def decode_wx_phenomena(self, enc):
    pass

  def decode_sky_condition(self, enc):
    pass

  def decode_temp(self, enc):
    pass

  def decode_dewpoint(self, enc):
    pass

  def decode_altimeter(self, enc):
    pass

  def decode_remarks(self, enc):
    pass

  def decode_tornadic_activity(self, enc):
    pass

  def decode_stn_type(self, enc):
    pass

  def decode_peak_wind(self, enc):
    pass

  def decode_wind_shift(self, enc):
    pass

  def decode_variable_vis(self, enc):
    pass

  def decode_vis_second_loc(self, enc):
    pass

  def decode_lightning(self, enc):
    pass

  def decode_precip_ts(self, enc):
    pass

  def decode_virga(self, enc):
    pass

  def decode_variable_ceiling(self, enc):
    pass

  def decode_ceiling_second_loc(self, enc):
    pass

  def decode_pressure_rise_fall_rapid(self, enc):
    pass

  def decode_sea_level_pressure(self, enc):
    pass

  def decode_hourly_precip(self, enc):
    pass

  def decode_three_six_hour_precip(self, enc):
    pass

  def decode_twenty_four_hour_precip(self, enc):
    pass

  def decode_pressure_tendency(self, enc):
    pass

  def decode_sensor_status(self, enc):
    pass

  def decode_maint_reqd(self, enc):
    pass

  def __init__(self):
    print ">>> called decode metar"
