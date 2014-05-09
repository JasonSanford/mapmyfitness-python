import unittest

from mapmyfitness import MapMyFitness


class MapMyFitnessTestCase(unittest.TestCase):
    uri_root = 'https://oauth2-api.mapmyapi.com/v7.0'
    def setUp(self):
        self.mmf = MapMyFitness(api_key='abc123', access_token='super-secret-token')


class MapMyFitnessTestCaseCacheFinds(unittest.TestCase):
    uri_root = 'https://oauth2-api.mapmyapi.com/v7.0'
    def setUp(self):
        self.mmf = MapMyFitness(api_key='abc123', access_token='super-secret-token', cache_finds=True)
