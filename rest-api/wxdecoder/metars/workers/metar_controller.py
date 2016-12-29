from metar_parser import MetarParser
from metar_decoder import MetarDecoder
from avwx_proxy import AVWXProxy

class MetarController:

  def decode_metar(self, raw_metar):
    # TODO: needs unit test
    json_metar = self.parse_raw_metar_to_json(raw_metar)
    json_decoded_metar = self.decode_json_metar(json_metar)
    json_decoded_metar["raw_metar"] = raw_metar
    return json_decoded_metar

  def retrieve_and_decode_metar(self, airport_id):
    raw_metar = self.get_metar_for_airport_id(airport_id)
    return self.decode_metar(raw_metar)

  def parse_raw_metar_to_json(self, raw_metar):
    parser = MetarParser()
    res = parser.parse_metar(raw_metar)
    return parser.parse_metar(raw_metar)

  def decode_json_metar(self, json_metar):
    decoder = MetarDecoder()
    return decoder.decode_metar(json_metar)

  def get_metar_for_airport_id(self, airport_id):
    avwx_proxy = AVWXProxy()
    return avwx_proxy.get_metar_for_airport_id(airport_id)
