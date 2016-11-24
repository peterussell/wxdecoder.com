class MetarDecoder:

  def __init__(self):
    print ">>> Initializing MetarDecoder"

  def decode_metar(self, raw_metar):
    print ">>> Decoding METAR: %s" % raw_metar
    parts = raw_metar.split()
    print ">>> METAR parts:\n>>> %s" % parts

  # METAR components. See http://www.met.tamu.edu/class/metar/quick-metar.html.
  icao_id = ''
  obs_datetime = None
  mod_auto = ''
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
