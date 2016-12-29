import requests

AVWX_ROOT_URL = 'https://avwx.rest/api/metar/'

class AVWXProxy:

  def get_metar_for_airport_id(self, airport_id):
    # TODO: need some validation airport_id is valid here
    url = '%s%s' % (AVWX_ROOT_URL, airport_id)
    res = requests.get(url)
    if res.status_code != 200:
      print "Error calling AVWXProxy - response status code: %" % res.status_code
      # TODO: we should log/raise this error
      return ""
    raw_metar = res.json()['Raw-Report']
    return raw_metar
