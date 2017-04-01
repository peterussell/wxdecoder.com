import json

class MetarParser:

  def parse_metar(self, raw_metar):
    tokens = raw_metar.split()
    return self.parse_tokens(tokens)

  def parse_tokens(self, tokens):
    # Each parser gets called in turn. If the next token of the METAR matches
    # what that parser expects, it parses the relevant section (or sections),
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
    tokens = self.parse_remarks(tokens)

    # Store any remaining tokens as remarks (for now)
    self.parsed_metar["misc"] = ' '.join(tokens)

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
      # Loop until we run out of WX phenomena tokens
      if self.is_wx_phenomena_token(t):
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

  def parse_remarks(self, tokens):
    if 'RMK' not in tokens:
      return tokens

    # Ignore any tokens before RMK
    rmk_index = tokens.index('RMK')
    rmk_tokens = tokens[rmk_index+1:]

    processed_tokens = []
    for rt in rmk_tokens:
      if rt == 'RMK':
        processed_tokens.append(rt)
      # Station type
      if rt.startswith('A0'):
        processed_tokens.append(self.parse_rmk_stn_type(rt))
      # Peak wind
      if rt == 'PK':
        processed_tokens.extend(
          self.parse_rmk_peak_wind(rmk_tokens, rmk_tokens.index(rt)))
      # Wind shift
      if rt == 'WSHFT':
        processed_tokens.extend(
          self.parse_rmk_wind_shift(rmk_tokens, rmk_tokens.index(rt)))
      # Pressure - rapid rise or fall
      if rt.startswith('PRES'):
        processed_tokens.append(self.parse_rmk_pressure_rise_fall_rapid(rt))
      # Sea level pressure
      if rt.startswith('SLP'):
        processed_tokens.append(self.parse_rmk_sea_level_pressure(rt))
      # Maintenance required
      if rt == '$':
        processed_tokens.append(self.parse_rmk_maint_reqd(rt))

    unprocessed_tokens = [ t for t in rmk_tokens if t not in processed_tokens ]

    # Result:
    #  -> Any remarks we could process are copied to their respective fields and
    #     removed from parsed_metar["remarks"].
    #  -> parsed_metar["remarks"] contains any tokens after RMK we couldn't process.
    #  -> Return any tokens preceding RMK, we don't know what they are.
    self.parsed_metar["remarks"] = ' '.join(unprocessed_tokens)
    return tokens[:rmk_index]

  ### Remarks Parser Helpers
  def parse_rmk_stn_type(self, token):
    if token == 'A01' or token == 'A02':
      self.parsed_metar["stn_type"] = token
      return token

  def parse_rmk_peak_wind(self, tokens, start_index):
    if tokens[start_index] == 'PK' and tokens[start_index+1] == 'WND':
      # Expect three tokens: 'PK', 'WND', and the value
      pk_wnd_toks = tokens[start_index:start_index+3]
      self.parsed_metar["peak_wind"] = ' '.join(pk_wnd_toks)
      return pk_wnd_toks

  def parse_rmk_wind_shift(self, tokens, start_index):
    # Format: WSHFT <time> [FROPA]
    ws_tokens = tokens[start_index:start_index+2]
    if start_index+2 < len(tokens) and tokens[start_index+2] == 'FROPA':
      ws_tokens.append('FROPA')
    self.parsed_metar["wind_shift"] = ' '.join(ws_tokens)
    print ws_tokens
    return ws_tokens

  def parse_rmk_pressure_rise_fall_rapid(self, token):
    if token == 'PRESRR' or token == 'PRESFR':
      self.parsed_metar["pressure_rise_fall_rapid"] = token
      return token

  def parse_rmk_sea_level_pressure(self, token):
    if token.startswith('SLP'):
      self.parsed_metar["sea_level_pressure"] = token
      return token

  def parse_rmk_maint_reqd(self, token):
    if token == '$':
      self.parsed_metar["maint_reqd"] = True
      return token

  ### Helpers - TODO: Move to utils module
  def is_wx_phenomena_token(self, token):
    if (token.startswith('-') or \
        token.startswith('+') or \
        token.startswith('VC')):
      return True
    WX_PHENOMENA = ['DZ','RA','SN','SG','IC','PE','GR','GS',
                    'BR','FG','FU','VA','DU','SA','HZ','PY',
                    'PO','SQ','FC','SS','DS']
    for wxp in WX_PHENOMENA:
      if wxp in token:
        return True
    return False

  def is_sky_condition_token(self, token):
    if token.startswith('CLR') or \
       token.startswith('FEW') or \
       token.startswith('SCT') or \
       token.startswith('BKN') or \
       token.startswith('OVC') or \
       token.startswith('VV'):
      return True
    return False

  def __init__(self):
    # Set default METAR components. See http://www.met.tamu.edu/class/metar/quick-metar.html
    with open('metars/workers/data/metar-defaults.json') as metar_file:
      contents = json.load(metar_file)
      self.parsed_metar = contents["metar"]
