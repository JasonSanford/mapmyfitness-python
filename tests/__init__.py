import unittest

from mapmyfitness import MapMyFitness
from mapmyfitness.api import APIConfig
from mapmyfitness.exceptions import InvalidAPIVersionException


class APIConfigTest(unittest.TestCase):
    def test_invalid_version(self):
        try:
            APIConfig(access_token='foo', version=99)
        except Exception as exc:
            self.assertIsInstance(exc, InvalidAPIVersionException)


class FulcrumTestCase(unittest.TestCase):
    api_root = 'https://api.mapmyapi.com/v7.0'

    def setUp(self):
        self.mmf_api = MapMyFitness(access_token='super-secret-token')