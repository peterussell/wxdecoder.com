# NB. This function doesn't validate raw_metar is actually a METAR.
# It just strips a leading 'METAR' or 'SPECI', then returns the
# next token (space-delimited).
def get_icao_id_from_raw_metar(raw_metar):
  # Strip METAR or SPECI if we have it
  if raw_metar.startswith("METAR") or raw_metar.startswith("SPECI"):
    raw_metar = raw_metar[len("METAR "):]
  return raw_metar[:raw_metar.find(' ')]
