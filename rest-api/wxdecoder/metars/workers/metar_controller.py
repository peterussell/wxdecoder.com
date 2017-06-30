from parsers.mp_default import MetarParserDefault
from decoders.md_default import MetarDecoderDefault
from parsers.mp_nz import MetarParserNZ
from decoders.md_nz import MetarDecoderNZ
from avwx_proxy import AVWXProxy
import utils

class MetarController:

  def retrieve_and_decode_metar(self, airport_id):
    raw_metar = self.get_metar_for_airport_id(airport_id)
    return self.decode_metar(raw_metar)

  def get_metar_for_airport_id(self, airport_id):
    avwx_proxy = AVWXProxy()
    return avwx_proxy.get_metar_for_airport_id(airport_id)

  def decode_metar(self, raw_metar):
    country = self._get_country_from_raw_metar(raw_metar)
    json_metar = self.parse_raw_metar_to_json(raw_metar, country)
    json_decoded_metar = self.decode_json_metar(json_metar, country)
    json_decoded_metar["raw_metar"] = raw_metar
    return json_decoded_metar

  def parse_raw_metar_to_json(self, raw_metar, country):
    parser = self._get_parser_for_country(country)
    res = parser.parse_metar(raw_metar)
    return parser.parse_metar(raw_metar)

  def decode_json_metar(self, json_metar, country):
    decoder = self._get_decoder_for_country(country)
    return decoder.decode_metar(json_metar)

  # -------- Country-Specific Helpers -------
  def _get_country_from_raw_metar(self, raw_metar):
    icao_id = utils.get_icao_id_from_raw_metar(raw_metar)
    if icao_id.startswith('NZ'):
      return 'NZ'
    return 'US' # default

  def _get_parser_for_country(self, country):
    if country is 'US':
      return MetarParserDefault()
    if country is 'NZ':
      return MetarParserNZ()

  def _get_decoder_for_country(self, country):
    if country is 'US':
      return MetarDecoderDefault()
    if country is 'NZ':
      return MetarDecoderNZ()
