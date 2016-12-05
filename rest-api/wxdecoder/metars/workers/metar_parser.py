import json

class MetarParser:

  def parse_metar(self, raw_metar):
    tokens = raw_metar.split()
    return self.parse_tokens(tokens)

  def parse_tokens(self, tokens):
    # Each parseor gets called in turn. If the next token of the METAR matches
    # what that parseor expects, it parses the relevant section (or sections),
    # stores the parsed result in the relevant class field, strips the token(s)
    # from the METAR and returns the result

    # If the token doesn't match what it each parseor expects we can assume
    # it's been omitted from the METAR and return immediately.
    tokens = self.parse_metar_header(tokens)
    tokens = self.parse_icao_id(tokens)
    tokens = self.parse_datetime(tokens)
    tokens = self.parse_automated_obs_flag(tokens)
    tokens = self.parse_wind_dir_speed(tokens)
    tokens = self.parse_wind_dir_variation(tokens)
    tokens = self.parse_visibility(tokens)
    tokens = self.parse_rvr(tokens)
    tokens = self.parse_wx_phenomena(tokens)
    tokens = self.parse_sky_condition(tokens)
    tokens = self.parse_temp_dewpoint(tokens)
    tokens = self.parse_altimeter(tokens)

    # Store any remaining tokens as remarks (for now)
    self.parsed_metar["remarks"] = ' '.join(tokens)

    # Return any remaining tokens
    return self.parsed_metar

  def parse_metar_header(self, tokens):
    if tokens[0] == 'METAR':
      tokens.pop(0)
    elif tokens[0] == 'SPECI':
      self.parsed_metar["is_special_report"] = True
      tokens.pop(0)
    return tokens

  def parse_icao_id(self, tokens):
    self.parsed_metar["icao_id"] = tokens.pop(0)
    return tokens

  def parse_datetime(self, tokens):
    if tokens[0].endswith('Z'):
      self.parsed_metar["obs_datetime"] = tokens.pop(0)
    return tokens

  def parse_automated_obs_flag(self, tokens):
    if tokens[0] == 'AUTO':
      self.parsed_metar["mod_auto"] = True
      tokens.pop(0)
    return tokens

  def parse_wind_dir_speed(self, tokens):
    if "KT" in tokens[0]:
      self.parsed_metar["wind_dir_speed"] = tokens.pop(0)
    return tokens

  def parse_wind_dir_variation(self, tokens):
    if "V" in tokens[0]:
      self.parsed_metar["wind_dir_variation"] = tokens.pop(0)
    return tokens

  def parse_visibility(self, tokens):
    if tokens[0].endswith('SM'):
      self.parsed_metar["vis"] = tokens.pop(0)
    return tokens

  def parse_rvr(self, tokens):
    if tokens[0].startswith('R') and tokens[0].endswith('FT'):
      self.parsed_metar["rvr"] = tokens.pop(0)
    return tokens

  def parse_wx_phenomena(self, tokens):
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
    self.parsed_metar["wx_phenomena"] = list(wx_tokens)
    return tokens

  def parse_sky_condition(self, tokens):
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
    self.parsed_metar["sky_condition"] = list(sky_con_tokens)
    return tokens

  def parse_temp_dewpoint(self, tokens):
    if '/' in tokens[0]:
      parts = tokens.pop(0).split('/')
      self.parsed_metar["temp"] = parts[0]
      self.parsed_metar["dewpoint"] = parts[1]
    return tokens

  def parse_altimeter(self, tokens):
    if tokens[0].startswith('A'):
      tok = tokens.pop(0)
      self.parsed_metar["altimeter"] = tok.replace('A', '')
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

  def __init__(self):
    # Set default METAR components. See http://www.met.tamu.edu/class/metar/quick-metar.html
    with open('metar.json') as metar_file:
      contents = json.load(metar_file)
      self.parsed_metar = contents["metar"]
