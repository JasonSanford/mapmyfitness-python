import httpretty

from mapmyfitness.exceptions import InvalidSearchArgumentsException

from tests import MapMyFitnessTestCase


class RouteTest(MapMyFitnessTestCase):
    def test_no_filter(self):
        try:
            routes = self.mmf_api.route.all()
        except Exception as exc:
            self.assertIsInstance(exc, InvalidSearchArgumentsException)
            self.assertEqual(str(exc), 'Either a user, users or close_to_location argument must be passed to search for routes.')