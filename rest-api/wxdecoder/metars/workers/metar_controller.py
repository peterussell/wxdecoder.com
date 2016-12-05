from metar_parser import MetarParser

class MetarController:

  def decode_metar(self, raw_metar):
    print ">>> Calling decode_metar"
    print "> raw_metar\n%s" % raw_metar

    json_metar = parse_raw_metar_to_json(raw_metar)
    print "> json_metar:\n%s" % json_metar

    json_decoded_metar = decode_json_metar(json_metar)
    print "> json_decoded_metar:\n%s" % json_decoded_metar

    return json_decoded_metar

  def parse_raw_metar_to_json(self, raw_metar):
    parser = MetarParser()
    res = parser.parse_metar(raw_metar)
    return parser.parse_metar(raw_metar)

  def decode_json_metar(self, json_metar):
    decoder = MetarDecoder()
    return decoder.decode_json_metar(json_metar)
