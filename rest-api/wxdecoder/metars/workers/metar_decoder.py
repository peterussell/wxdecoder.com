# -*- coding: utf-8 -*-

import json
import locale

class MetarDecoder:

  DECODED_KEY = "decoded"

  def decode_metar(self, json_metar):
    print ">>> %s \n\n\n <<<" % json_metar
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
    return self.decoded_metar

  def decode_is_special_report(self, val):
    key = "is_special_report"
    self.copy_orig_value(key, val)
    self.decoded_metar[key][self.DECODED_KEY] = val

  def decode_icao_id(self, val):
    key = "icao_id"
    self.copy_orig_value(key, val)
    self.decoded_metar[key][self.DECODED_KEY] = val

  def decode_obs_datetime(self, val):
    key = "obs_datetime"
    self.copy_orig_value(key, val)
    self.decoded_metar[key][self.DECODED_KEY]["date"] = val[:2]
    self.decoded_metar[key][self.DECODED_KEY]["time"] = val[2:-1]

  def decode_mod_auto(self, val):
    key = "mod_auto"
    self.copy_orig_value(key, val)
    self.decoded_metar[key][self.DECODED_KEY] = val

  def decode_wind_dir_speed(self, val):
    key = "wind_dir_speed"
    self.copy_orig_value(key, val)

    # Handle calm winds
    if val == "00000KT":
      self.decoded_metar[key][self.DECODED_KEY] = \
        "calm winds"
      return

    # Handle light and variable winds (1KTS < wind < 7KTS)
    if val.startswith("VRB"):
      kt_index = val.find("KT")
      speed = val[4:kt_index].lstrip("0")
      speed_unit = self.get_pluralized_unit(speed, "knot")
      self.decoded_metar[key][self.DECODED_KEY] = \
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
    speed_unit = self.get_pluralized_unit(speed, "knot")

    # Assemble the output
    res = "from %s degrees, at %s %s" % (direction, speed, speed_unit)
    if has_gusts:
      res += " gusting to %s knots" % gust

    self.decoded_metar[key][self.DECODED_KEY] = res

  def decode_wind_dir_variation(self, val):
    key = "wind_dir_variation"
    self.copy_orig_value(key, val)
    if val == "": return

    d_from, d_to = val.split('V')
    self.decoded_metar[key][self.DECODED_KEY] = \
      "variable, from %s degrees to %s degrees" % (d_from, d_to)

  def decode_vis(self, val):
    key = "vis"
    self.copy_orig_value(key, val)

    sm_index = val.find("SM")
    # Handle vis < 1/4SM ("M1/4SM")
    if val.startswith("M"):
      vis_dist = val[1:sm_index]
      self.decoded_metar["vis"][self.DECODED_KEY] = \
        "less than %s statute mile" % vis_dist
      return

    vis_dist = val[:sm_index]
    vis_unit = self.get_pluralized_unit(vis_dist, "statute mile")
    self.decoded_metar["vis"][self.DECODED_KEY] = \
      "%s %s" % (vis_dist, vis_unit)

  def decode_rvr(self, val):
    key = "rvr"
    self.copy_orig_value(key, val)
    if val == "": return

    parts = val.split("/")
    rwy_part = parts[0].strip()
    rvr_part = parts[1].strip()
    trend_part = None
    if len(parts) == 3:
      trend_part = parts[2].strip()

    res_rwy = ""
    res_modifier = ""
    res_rvr = ""
    res_trend = ""

    # Runway
    res_rwy = rwy_part[1:]

    # Modifiers
    if rvr_part.startswith("M"):
      res_modifier = "less than "
      rvr_part = rvr_part[1:]
    if rvr_part.startswith("P"):
      res_modifier = "more than "
      rvr_part = rvr_part[1:]

    ft_index = rvr_part.find("FT")

    # RVR - variable
    if rvr_part.find("V") != -1: # has a variable component
      variable_from, variable_to = rvr_part.split("V")
      ft_index_variable = variable_to.find("FT")
      # Insert some commas
      variable_from = self.localize_num(variable_from[:ft_index])
      variable_to = self.localize_num(variable_to[:ft_index_variable])
      res_rvr = "variable, from %s to %s feet" % \
        (variable_from, variable_to)

    # RVR - non-variable
    else:
      res_rvr = "%s feet" % self.localize_num(rvr_part[:ft_index])

    # Trend
    if trend_part:
      if trend_part == "D":
        res_trend = ", trending downward"
      elif trend_part == "U":
        res_trend = ", trending upward"
      elif trend_part == "N":
        res_trend = ", no change"

    # Put it together...
    self.decoded_metar[key][self.DECODED_KEY] = \
      "%s%s%s (runway %s)" % (res_modifier, res_rvr, res_trend, res_rwy)

  def decode_wx_phenomena(self, val):
    key = "wx_phenomena"
    self.copy_orig_value(key, val)
    del self.decoded_metar[key][self.DECODED_KEY][:]

    # Load the mappings (METAR code -> plain English)
    with open('metars/workers/data/wx-phenomena.json') as wxp:
      mappings = json.load(wxp)["codes"]

    for full_token in val:
      decoded_wx = []

      # Find the modifier (light, moderate, heavy, in the vicinity)
      post_mod = ""
      if full_token.startswith("+FC"):
        # Special case for '+FC' (tornados/waterspouts)
        self.decoded_metar[key][self.DECODED_KEY].append(mappings["+FC"])
        continue
      elif full_token.startswith("-"):
        decoded_wx.append("light")
        full_token = full_token[1:]
      elif full_token.startswith("+"):
        decoded_wx.append("heavy")
        full_token = full_token[1:]
      elif full_token.startswith("VC"):
        post_mod = "in the vicinity" # save post modifiers to be appended after other tokens
        full_token = full_token[2:]
      else:
        decoded_wx.append("moderate")

      # Split the code into 2-char pieces
      tokens = [full_token[i:i+2] for i in range(0, len(full_token), 2)]

      # For each piece of the phenomenon, check if it exists in the mappings;
      # if so, save the english equivalent.
      for token in tokens:
        if token in mappings:
          decoded_wx.append(mappings[token])
      else:
        # TODO: got a WX phenomena we can't identify, should log or throw an error
        pass

      # Add the post modifiers
      if post_mod != "":
        decoded_wx.append(post_mod)

      # Put it together...
      self.decoded_metar[key][self.DECODED_KEY].append(" ".join(decoded_wx))

  def decode_sky_condition(self, val):
    key = "sky_condition"
    self.copy_orig_value(key, val)
    del self.decoded_metar[key][self.DECODED_KEY][:]

    for layer in val:
      decoded_layer = ""

      # Layer type
      layer_type_len = 3 # default (FEW, SCT, BKN, OVC)

      # Start with special cases SKC and CLR. They have no altitude
      # value so just save them and move to the next layer
      if layer.startswith("SKC"):
        self.decoded_metar[key][self.DECODED_KEY].append("sky clear")
        continue
      elif layer.startswith("CLR"):
        self.decoded_metar[key][self.DECODED_KEY].append( \
          "no clouds below 12,000 feet")
        continue

      # Handle indefinite ceiling and change the prefix length to 2
      elif layer.startswith("VV"):
        decoded_layer += "vertical visibility (indefinite ceiling)"
        layer_type_len = 2

      # Handle 'standard' cases (FEW, SCT, BKN, OVC)
      elif layer.startswith("FEW"):
        decoded_layer += "few clouds"
      elif layer.startswith("SCT"):
        decoded_layer += "scattered clouds"
      elif layer.startswith("BKN"):
        decoded_layer += "broken clouds"
      elif layer.startswith("OVC"):
        decoded_layer += "overcast"

      # Check for a cumulonimbus or towering cumulus modifier
      is_cb = False
      is_tcu = False
      modifier_len = 0 # default
      if layer.endswith("CB"):
        is_cb = True
        modifier_len = 2
      if layer.endswith("TCU"):
        is_tcu = True
        modifier_len = 3

      # Altitude (anything else)
      altitude = layer[layer_type_len:len(layer)-modifier_len]

      # Special case: "///" = cloud layer below station
      if altitude == "///":
        decoded_layer += " below reporting station elevation"
      else:
        altitude = altitude.lstrip("0")
        try:
          int_alt = int(altitude) * 100
          localized_alt = self.localize_num(int_alt)
          decoded_layer += " at %s feet" % localized_alt
        except ValueError:
          # TODO: couldn't convert altitude to an int, log or throw
          pass

      # Add on the cumulonimbus/towering cumulus modifiers
      if is_cb:
        decoded_layer += " (cumulonimbus)"
      if is_tcu:
        decoded_layer += " (towering cumulus)"

      # Put it together...
      self.decoded_metar[key][self.DECODED_KEY].append(decoded_layer)

  def decode_temp(self, val):
    key = "temp"
    self.copy_orig_value(key, val)
    self.decoded_metar[key][self.DECODED_KEY] = self.get_decoded_temp_str(val)

  def decode_dewpoint(self, val):
    key = "dewpoint"
    self.copy_orig_value(key, val)
    self.decoded_metar[key][self.DECODED_KEY] = self.get_decoded_temp_str(val)

  # Shared decoder for temperature and dewpoint
  def get_decoded_temp_str(self, val):
    if val == "":
      return "(missing)"

    res = ""
    if val.startswith("M"):
      res += "minus "
      val = val[1:]

    val = val.lstrip("0")
    degree_sign = u'\N{DEGREE SIGN}'
    res += "%s%sC" % (val, degree_sign)
    return res

  def decode_altimeter(self, val):
    key = "altimeter"
    self.copy_orig_value(key, val)
    val = val.lstrip("A")
    self.decoded_metar[key][self.DECODED_KEY] = \
      "%s.%s\"Hg" % (val[:2], val[2:])

  def decode_remarks(self, val):
    key = "remarks"
    self.copy_orig_value(key, val)
    # For now just copy the whole remarks section to the decoded field
    self.decoded_metar[key][self.DECODED_KEY] = val

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

  def get_pluralized_unit(self, val, unit):
    default_res = "%ss" % unit # default to pluralized unit
    try:
      int_val = int(val)
      if int_val == 1:
        return unit
      else:
        return default_res
    except ValueError:
      return default_res

  def localize_num(self, val):
    return locale.format("%d", int(val), grouping=True)

  def __init__(self):
    # Load defaults

    # tmp
    import os
    print ">>> %s " % os.getcwd()

    with open('metars/workers/data/metar-decoded-defaults.json') as decoded_metar_file:
      contents = json.load(decoded_metar_file)
      self.decoded_metar = contents["metar"]
    locale.setlocale(locale.LC_ALL, 'en_US')
