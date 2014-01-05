import copy

import httpretty

from mapmyfitness.exceptions import InvalidSearchArgumentsException, InvalidObjectException

from tests import MapMyFitnessTestCase
from tests.valid_objects import route as valid_route


class RouteTest(MapMyFitnessTestCase):
    def test_no_filter(self):
        try:
            routes = self.mmf.route.all()
        except Exception as exc:
            self.assertIsInstance(exc, InvalidSearchArgumentsException)
            self.assertEqual(str(exc), 'Either a user, users or close_to_location argument must be passed to search for routes.')

    def test_create_no_name(self):
        a_route = copy.deepcopy(valid_route)
        del a_route['name']
        try:
            route = self.mmf.route.create(a_route)
        except Exception as exc:
            self.assertIsInstance(exc, InvalidObjectException)
            self.assertEqual(str(exc), 'Route name must exist and be of type str.')

    def test_create_no_distance(self):
        a_route = copy.deepcopy(valid_route)
        del a_route['distance']
        try:
            route = self.mmf.route.create(a_route)
        except Exception as exc:
            self.assertIsInstance(exc, InvalidObjectException)
            self.assertEqual(str(exc), 'Route distance must exist and be of type int or float.')