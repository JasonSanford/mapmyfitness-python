import unittest

from mapmyfitness import MapMyFitness


class MapMyFitnessTestCase(unittest.TestCase):
    uri_root = 'https://oauth2-api.mapmyapi.com/v7.0'
    def setUp(self):
        self.mmf = MapMyFitness(api_key='abc123', access_token='super-secret-token')

    def test_MapMyFitness_is_singleton(self):
        mmf1 = MapMyFitness('api-key1', 'access_token1')
        mmf2 = MapMyFitness('api-key2', 'access_token2')
        
        assert mmf1 == mmf2
