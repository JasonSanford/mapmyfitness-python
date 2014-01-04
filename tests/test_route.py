import httpretty

from mapmyfitness.exceptions import InvalidSearchArgumentsException

from tests import MapMyFitnessTestCase

# route 400
obj = {u'_diagnostics': {u'validation_failures': [[u'a filter is required: (user, users, close_to_location)']]}, u'_links': {u'self': [{u'href': u'/v7.0/route/?limit=20&offset=0'}], u'documentation': [{u'href': u'https://developer.mapmyapi.com/docs/Route'}]}}


class RouteTest(MapMyFitnessTestCase):
    def test_no_filter(self):
        try:
            routes = self.mmf_api.route.all()
        except Exception as exc:
            self.assertIsInstance(exc, InvalidSearchArgumentsException)
            self.assertEqual(str(exc), 'Either a user, users or close_to_location argument must be passed to search for routes.')