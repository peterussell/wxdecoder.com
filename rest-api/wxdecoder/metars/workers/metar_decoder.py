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

    # If the token doesn't match what it expects we can assume it's been omitted
    # from the METAR and just return from the processor without doing anything.
    tokens = self.process_metar_header(tokens)
    tokens = self.process_iaao_id(tokens)

    # Return any remaining tokens
    return tokens # tmp - not sure what we want to return here

  def process_metar_header(self, tokens):
    if tokens[0] == 'METAR':
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

  # METAR components. See http://www.met.tamu.edu/class/metar/quick-metar.html.
  icao_id = ''
  obs_datetime = None
  mod_auto = False
  wind_dir_speed = ''
  vis = ''
  rvr = ''
  wx_phenomena = []
  skc = []
  temp = ''
  dewpoint = ''
  altimeter = ''
  remarks = ''
  tornadic_activity = []
  stn_type = ''
  peak_wind = ''
  wind_shift = ''
  variable_vis = ''
  vis_second_loc = ''
  lightning = []
  precip_ts = []
  virga = ''
  variable_ceilingg = ''
  ceiling_second_loc = ''
  press_rise_fall_rapid = ''
  sea_level_press = ''
  hourly_precip = ''
  three_six_hour_precip = []
  twenty_four_hour_precip = []
  press_tendency = ''
  sensor_status = []
  maint_reqd = ''
