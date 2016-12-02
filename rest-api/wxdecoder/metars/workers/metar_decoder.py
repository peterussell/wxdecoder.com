class MetarDecoder:

  def __init__(self):
    print ">>> Initializing MetarDecoder"

  def decode_metar(self, raw_metar):
    print ">>> Decoding METAR: %s" % raw_metar
    tokens = raw_metar.split()
    tokens = self.process_tokens(tokens)
    # TODO: assert that the tokens length is 0

    # TODO: process the fields, concatenate them nicely, and return the output
    return raw_metar # tmp

  def process_tokens(self, tokens):
    # Each processor gets called in turn. If the next token of the METAR matches
    # what that processor expects, it decodes the relevant section (or sections),
    # stores the decoded result in the relevant class field, strips the tokens
    # from the METAR and returns the result

    # If the token doesn't match what it each processor expects we can assume
    # it's been omitted from the METAR and return immediately.
    tokens = self.process_metar_header(tokens)
    tokens = self.process_icao_id(tokens)
    tokens = self.process_datetime(tokens)
    tokens = self.process_automated_obs_flag(tokens)
    tokens = self.process_wind_dir_speed(tokens)
    tokens = self.process_wind_dir_variation(tokens)
    tokens = self.process_visibility(tokens)
    tokens = self.process_rvr(tokens)
    tokens = self.process_wx_phenomena(tokens)
    tokens = self.process_sky_condition(tokens)
    tokens = self.process_temp_dewpoint(tokens)
    tokens = self.process_altimeter(tokens)

    # Store any remaining tokens as remarks (for now)
    self.remarks = ' '.join(tokens)

    # Return any remaining tokens
    return tokens # tmp - not sure what we want to return here

  def process_metar_header(self, tokens):
    if tokens[0] == 'METAR':
      tokens.pop(0)
    elif tokens[0] == 'SPECI':
      self.is_special_report = True
      tokens.pop(0)
    return tokens

  def process_icao_id(self, tokens):
    self.icao_id = tokens.pop(0)
    return tokens

  def process_datetime(self, tokens):
    if tokens[0].endswith('Z'):
      self.obs_datetime = tokens.pop(0)
    return tokens

  def process_automated_obs_flag(self, tokens):
    if tokens[0] == 'AUTO':
      self.mod_auto = True
      tokens.pop(0)
    return tokens

  def process_wind_dir_speed(self, tokens):
    if "KT" in tokens[0]:
      self.wind_dir_speed = tokens.pop(0)
    return tokens

  def process_wind_dir_variation(self, tokens):
    if "V" in tokens[0]:
      self.wind_dir_variation = tokens.pop(0)
    return tokens

  def process_visibility(self, tokens):
    if tokens[0].endswith('SM'):
      self.vis = tokens.pop(0)
    return tokens

  def process_rvr(self, tokens):
    if tokens[0].startswith('R') and tokens[0].endswith('FT'):
      self.rvr = tokens.pop(0)
    return tokens

  def process_wx_phenomena(self, tokens):
    wx_tokens = []
    for t in tokens:
      # Loop until we get a sky condition token.
      # Note: this will break if the sky condition is omitted (TODO, revisit).
      # One solution would be implement 'is_wx_phenomena_token(token)', but that
      # could be expensive given how many tokens there are; it's cheaper to
      # check the much smaller sky condition list.
      if not self.is_sky_condition_token(t):
        wx_tokens.append(t)
      else:
        break
    # Remove the tokens from the original tokens list (we avoid doing this
    # while iterating the original list).
    for wxt in wx_tokens:
      tokens.remove(wxt)
    self.wx_phenomena = list(wx_tokens)
    return tokens

  def process_sky_condition(self, tokens):
    sky_con_tokens = []
    for t in tokens:
    # Loop until we _don't_ get a sky condition token.
      if self.is_sky_condition_token(t):
        sky_con_tokens.append(t)
      else:
        break
    # Remove tokens from the original tokens list
    for sct in sky_con_tokens:
      tokens.remove(sct)
    self.sky_condition = list(sky_con_tokens)
    return tokens

  def process_temp_dewpoint(self, tokens):
    if '/' in tokens[0]:
      parts = tokens.pop(0).split('/')
      self.temp = parts[0]
      self.dewpoint = parts[1]
    return tokens

  def process_altimeter(self, tokens):
    if tokens[0].startswith('A'):
      self.altimeter = tokens.pop(0)
    return tokens

  ### Helpers - TODO: Move to utils module
  def is_sky_condition_token(self, token):
    if token.startswith('CLR') or \
       token.startswith('FEW') or \
       token.startswith('SCT') or \
       token.startswith('BKN') or \
       token.startswith('OVC'):
      return True
    return False


  # METAR components. See http://www.met.tamu.edu/class/metar/quick-metar.html
  is_special_report = False
  icao_id = ''
  obs_datetime = None
  mod_auto = False
  wind_dir_speed = '' # TODO: this should probably be an object
  wind_dir_variation = '' # TODO this should be an attribute in he wind_dir_speed object
  vis = '' # TODO: could be an object (can include 'M' prefix to indicate <1/4SM)
  rvr = '' # TODO: could be an object, can include modifiers which we may want to store
  wx_phenomena = []
  sky_condition = []
  temp = ''
  dewpoint = ''
  altimeter = ''
  remarks = ''

  # This is all in the Remarks section, implementation coming to a future version near you.
  # tornadic_activity = []
  # stn_type = ''
  # peak_wind = ''
  # wind_shift = ''
  # variable_vis = ''
  # vis_second_loc = ''
  # lightning = []
  # precip_ts = []
  # virga = ''
  # variable_ceilingg = ''
  # ceiling_second_loc = ''
  # press_rise_fall_rapid = ''
  # sea_level_press = ''
  # hourly_precip = ''
  # three_six_hour_precip = []
  # twenty_four_hour_precip = []
  # press_tendency = ''
  # sensor_status = []
  # maint_reqd = ''
