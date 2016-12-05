from metar_parser import MetarParser

def decode_meatar(self, raw_metar):
  print ">>> Calling decode_metar"
  print "> raw_metar\n%s" % raw_metar

  parser = MetarParser()
  json_metar = parser.parse_raw_metar(raw_metar)
  print "> json_metar:\n%s" % json_metar

  decoder = MetarDecoder()
  json_decoded_metar = decoder.decode_json_metar(json_metar)
  print "> json_decode_metar:\n%s" % json_decoded_metar

  return json_decoded_metar
