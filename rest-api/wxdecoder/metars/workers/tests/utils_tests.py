from nose import with_setup
from nose.tools import assert_equals

import metars.workers.utils as utils

class TestUtils:

  @classmethod
  def setup_class(cls):
    pass

  def test_get_icao_id_from_raw_metar_no_metar_or_speci_text(self):
    metar = 'KSQL 280156Z 25014G19KT 10SM SCT013 16/12 A2995'
    res = utils.get_icao_id_from_raw_metar(metar)
    assert_equals(res, 'KSQL')

  def test_get_icao_id_from_raw_metar_preceding_metar_text(self):
    metar = 'METAR KMMV 280153Z AUTO 23010KT 10SM CLR 23/11 A2996'
    res = utils.get_icao_id_from_raw_metar(metar)
    assert_equals(res, 'KMMV')

  def test_get_icao_id_from_raw_metar_preceding_speci_text(self):
    metar = 'SPECI KOSH 280253Z 19005KT 10SM CLR 16/10 A2997'
    res = utils.get_icao_id_from_raw_metar(metar)
    assert_equals(res, 'KOSH')
