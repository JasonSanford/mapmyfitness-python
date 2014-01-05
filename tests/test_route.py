import copy

import httpretty

from mapmyfitness.exceptions import InvalidSearchArgumentsException, InvalidObjectException
from mapmyfitness.objects import RouteObject

from tests import MapMyFitnessTestCase
from tests.valid_objects import route as valid_route


class RouteTest(MapMyFitnessTestCase):
    def test_no_filter(self):
        try:
            self.mmf.route.all()
        except Exception as exc:
            self.assertIsInstance(exc, InvalidSearchArgumentsException)
            self.assertEqual(str(exc), 'Either a user, users or close_to_location argument must be passed to search for routes.')

    def test_create_no_name(self):
        a_route = copy.deepcopy(valid_route)
        del a_route['name']
        try:
            self.mmf.route.create(a_route)
        except Exception as exc:
            self.assertIsInstance(exc, InvalidObjectException)
            self.assertEqual(str(exc), 'Route name must exist and be of type str.')

    def test_create_no_distance(self):
        a_route = copy.deepcopy(valid_route)
        del a_route['distance']
        try:
            self.mmf.route.create(a_route)
        except Exception as exc:
            self.assertIsInstance(exc, InvalidObjectException)
            self.assertEqual(str(exc), 'Route distance must exist and be of type int or float.')

    def test_create_no_privacy(self):
        a_route = copy.deepcopy(valid_route)
        del a_route['privacy']
        try:
            self.mmf.route.create(a_route)
        except Exception as exc:
            self.assertIsInstance(exc, InvalidObjectException)
            self.assertEqual(str(exc), 'Route privacy must exist and be one of constants.PUBLIC, constants.PRIVATE or constants.FRIENDS.')

    @httpretty.activate
    def test_create_success(self):
        content_returned = '{"total_descent": null, "city": "Littleton", "data_source": null, "description": "This is a super-simplified route of my commute.", "updated_datetime": "2014-01-05T14:59:28.670550+00:00", "created_datetime": "2014-01-05T14:59:28.598493+00:00", "country": null, "start_point_type": "", "starting_location": {"type": "Point", "coordinates": [0, 0]}, "distance": 25749.5, "total_ascent": null, "climbs": null, "state": "CO", "points": [{"lat": 39.5735, "lng": -105.0164}, {"lat": 39.6781, "lng": -104.9926}, {"lat": 39.75009, "lng": -104.99656}], "postal_code": "", "min_elevation": null, "_links": {"documentation": [{"href": "https://developer.mapmyapi.com/docs/Route"}], "privacy": [{"href": "/v7.0/privacy_option/0/", "id": "0"}], "self": [{"href": "/v7.0/route/341663347/?field_set=detailed", "id": "341663347"}], "alternate": [{"href": "/v7.0/route/341663347/?format=kml&field_set=detailed", "id": "341663347", "name": "kml"}], "user": [{"href": "/v7.0/user/9118466/", "id": "9118466"}], "thumbnail": [{"href": "//images.mapmycdn.com/routes/thumbnail/341663347?size=100x100"}]}, "max_elevation": null, "name": "My Commute"}'
        uri = self.uri_root + '/route/?field_set=detailed'
        httpretty.register_uri(httpretty.POST, uri,
            body=content_returned,
            status=201)
        route = self.mmf.route.create(valid_route)
        self.assertIsInstance(route, RouteObject)
        self.assertEqual(route.name, valid_route['name'])
        self.assertEqual(route.description, valid_route['description'])
