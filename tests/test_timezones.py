from datetime import tzinfo, datetime, timedelta
import unittest

from mapmyfitness.timezones import utc


class MST(tzinfo):
    def utcoffset(self, dt):
      return timedelta(hours=-7)

    def dst(self, dt):
        timedelta(0)

mst = MST()


class TimezonesTest(unittest.TestCase):
    def test_timezones(self):
        mst_date = datetime(2014, 1, 6, 6, 28, 45, tzinfo=mst)
        utc_date = mst_date.astimezone(utc)
        self.assertEqual(utc_date.hour, 13)
        self.assertEqual(utc_date.tzname(), 'UTC')
