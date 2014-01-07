import copy
import json

import httpretty

from mapmyfitness.constants import PUBLIC
from mapmyfitness.exceptions import InvalidSearchArgumentsException, InvalidObjectException, ValidatorException
from mapmyfitness.objects import RouteObject
from mapmyfitness.serializers import RouteSerializer
from mapmyfitness.utils import iso_format_to_datetime
from mapmyfitness.validators import RouteValidator

from tests import MapMyFitnessTestCase
from tests.valid_objects import route as valid_route


class RouteTest(MapMyFitnessTestCase):
    def test_validator_bad_kwargs(self):
        try:
            RouteValidator()
        except Exception as exc:
            self.assertIsInstance(exc, ValidatorException)

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

    def test_create_bad_point(self):
        a_route = copy.deepcopy(valid_route)
        a_route['points'][0] = 'lobster'
        try:
            self.mmf.route.create(a_route)
        except Exception as exc:
            self.assertIsInstance(exc, InvalidObjectException)
            self.assertEqual(str(exc), 'Each point in Route points must be of type dict.')

    def test_create_bad_point_lat(self):
        a_route = copy.deepcopy(valid_route)
        a_route['points'][0]['lng'] = 'lobster'
        try:
            self.mmf.route.create(a_route)
        except Exception as exc:
            self.assertIsInstance(exc, InvalidObjectException)
            self.assertEqual(str(exc), 'Each point in Route points must have a "lng" key and be of type int or float.')

    def test_all_bad_user(self):
        try:
            self.mmf.route.all(user='lobster')
        except Exception as exc:
            self.assertIsInstance(exc, InvalidSearchArgumentsException)
            self.assertEqual(str(exc), 'Route user must be of type int.')

    def test_all_bad_users_not_list(self):
        try:
            self.mmf.route.all(users='lobsters')
        except Exception as exc:
            self.assertIsInstance(exc, InvalidSearchArgumentsException)
            self.assertEqual(str(exc), 'Route users must be a list or tuple of ints.')

    def test_all_bad_users_not_ints(self):
        try:
            self.mmf.route.all(users=(9118466, 'lobster'))
        except Exception as exc:
            self.assertIsInstance(exc, InvalidSearchArgumentsException)
            self.assertEqual(str(exc), 'Route users must be a list or tuple of ints.')

    """
    def test_all_user_success(self):
        routes = self.mm.route.all(user=9118466)
    """

    def test_all_close_to_location_latlng_not_list(self):
        try:
            self.mmf.route.all(close_to_location='lobsters')
        except Exception as exc:
            self.assertIsInstance(exc, InvalidSearchArgumentsException)
            self.assertEqual(str(exc), 'Route close_to_location must be a list or 2-tuple of latitude,longitude.')

    def test_all_close_to_location_latlng_not_floatable(self):
        try:
            self.mmf.route.all(close_to_location=(40.732, 'lobster'))
        except Exception as exc:
            self.assertIsInstance(exc, InvalidSearchArgumentsException)
            self.assertEqual(str(exc), 'Route close_to_location must be a list or 2-tuple of latitude,longitude.')

    def test_all_close_to_location_bad_distance(self):
        try:
            self.mmf.route.all(close_to_location=(40.732, -105), minimum_distance='lobster')
        except Exception as exc:
            self.assertIsInstance(exc, InvalidSearchArgumentsException)
            self.assertEqual(str(exc), 'Route minimum_distance must be of type int or float.')

    """
    def test_all_close_to_location_success(self):
        self.mmf.route.all(close_to_location=(40, -105))
    """

    @httpretty.activate
    def test_create_success(self):
        content_returned = '{"total_descent": null, "city": "Littleton", "data_source": null, "description": "This is a super-simplified route of my commute.", "updated_datetime": "2014-01-05T14:59:28.670550+00:00", "created_datetime": "2014-01-05T14:59:28.598493+00:00", "country": null, "start_point_type": "", "starting_location": {"type": "Point", "coordinates": [0, 0]}, "distance": 25749.5, "total_ascent": null, "climbs": null, "state": "CO", "points": [{"lat": 39.5735, "lng": -105.0164}, {"lat": 39.6781, "lng": -104.9926}, {"lat": 39.75009, "lng": -104.99656}], "postal_code": "", "min_elevation": null, "_links": {"documentation": [{"href": "https://developer.mapmyapi.com/docs/Route"}], "privacy": [{"href": "/v7.0/privacy_option/0/", "id": "0"}], "self": [{"href": "/v7.0/route/341663347/?field_set=detailed", "id": "341663347"}], "alternate": [{"href": "/v7.0/route/341663347/?format=kml&field_set=detailed", "id": "341663347", "name": "kml"}], "user": [{"href": "/v7.0/user/9118466/", "id": "9118466"}], "thumbnail": [{"href": "//images.mapmycdn.com/routes/thumbnail/341663347?size=100x100"}]}, "max_elevation": null, "name": "My Commute"}'
        uri = self.uri_root + '/route/?field_set=detailed'
        httpretty.register_uri(httpretty.POST, uri, body=content_returned, status=201)
        route = self.mmf.route.create(valid_route)
        self.assertIsInstance(route, RouteObject)
        self.assertEqual(route.name, valid_route['name'])

    @httpretty.activate
    def test_find(self):
        uri = self.uri_root + '/route/342208467'
        content_returned = '{"total_descent": null, "city": "Denver", "data_source": "run:RE", "description": "", "updated_datetime": "2014-01-06T22:26:50+00:00", "created_datetime": "2014-01-06T23:26:18+00:00", "country": "us", "start_point_type": "", "starting_location": {"type": "Point", "coordinates": [-104.99652, 39.7499]}, "points": null, "name": "Tuesday Lunch Run", "climbs": null, "state": "CO", "max_elevation": null, "postal_code": "80202", "min_elevation": null, "total_ascent": null, "_links": {"activity_types": [{"href": "/v7.0/activity_type/16/", "id": "16"}], "privacy": [{"href": "/v7.0/privacy_option/0/", "id": "0"}], "self": [{"href": "/v7.0/route/342208467/", "id": "342208467"}], "alternate": [{"href": "/v7.0/route/342208467/?format=kml&field_set=detailed", "id": "342208467", "name": "kml"}], "user": [{"href": "/v7.0/user/1/", "id": "1"}], "thumbnail": [{"href": "//images.mapmycdn.com/routes/thumbnail/342208467?size=100x100"}], "documentation": [{"href": "https://developer.mapmyapi.com/docs/Route"}]}, "distance": 5506.3582910718}'
        httpretty.register_uri(httpretty.GET, uri, body=content_returned, status=200)
        route = self.mmf.route.find(342208467)
        self.assertEqual(route.id, 342208467)

    @httpretty.activate
    def test_update(self):
        uri = self.uri_root + '/route/342208467/'
        update_with = {"privacy": PUBLIC, "total_descent": None, "city": "Denver", "data_source": "run:RE", "description": "Now you have a description.", "updated_datetime": "2014-01-06T22:26:50+00:00", "created_datetime": "2014-01-06T23:26:18+00:00", "country": "us", "start_point_type": "", "starting_location": {"type": "Point", "coordinates": [-104.99652, 39.7499]}, "points": [{"lat":39.5735,"lng":-105.0164},{"lat":39.6781,"lng":-104.9926},{"lat":39.75009,"lng":-104.99656}], "name": "Tuesday Lunch Run", "climbs": None, "state": "CO", "max_elevation": None, "postal_code": "80202", "min_elevation": None, "total_ascent": None, "_links": {"activity_types": [{"href": "/v7.0/activity_type/16/", "id": "16"}], "privacy": [{"href": "/v7.0/privacy_option/0/", "id": "0"}], "self": [{"href": "/v7.0/route/342208467/", "id": "342208467"}], "alternate": [{"href": "/v7.0/route/342208467/?format=kml&field_set=detailed", "id": "342208467", "name": "kml"}], "user": [{"href": "/v7.0/user/1/", "id": "1"}], "thumbnail": [{"href": "//images.mapmycdn.com/routes/thumbnail/342208467?size=100x100"}], "documentation": [{"href": "https://developer.mapmyapi.com/docs/Route"}]}, "distance": 5506.3582910718}
        content_returned = json.dumps(update_with)
        httpretty.register_uri(httpretty.PUT, uri, body=content_returned, status=200)
        route = self.mmf.route.update(342208467, update_with)
        self.assertEqual(route.description, 'Now you have a description.')

    @httpretty.activate
    def test_delete(self):
        uri = self.uri_root + '/route/1234'
        httpretty.register_uri(httpretty.DELETE, uri, status=204)
        deleted = self.mmf.route.delete(1234)
        self.assertIsNone(deleted)

    def test_serializer(self):
        json = {"total_descent":300,"city":"Littleton","data_source":None,"description":"This is a super-simplified route of my commute.","updated_datetime":"2014-01-05T14:59:28+00:00","created_datetime":"2014-01-05T14:59:28+00:00","country":"US","start_point_type":"","starting_location":{"type":"Point","coordinates":[0,0]},"distance":25749.5,"total_ascent":600,"climbs":None,"state":"CO","points":[{"lat":39.5735,"lng":-105.0164},{"lat":39.6781,"lng":-104.9926},{"lat":39.75009,"lng":-104.99656}],"postal_code":"","min_elevation":1500,"_links":{"documentation":[{"href":"https://developer.mapmyapi.com/docs/Route"}],"privacy":[{"href":"/v7.0/privacy_option/0/","id":"0"}],"self":[{"href":"/v7.0/route/341663347/?field_set=detailed","id":"341663347"}],"alternate":[{"href":"/v7.0/route/341663347/?format=kml&field_set=detailed","id":"341663347","name":"kml"}],"user":[{"href":"/v7.0/user/9118466/","id":"9118466"}],"thumbnail":[{"href":"//images.mapmycdn.com/routes/thumbnail/341663347?size=100x100"}]},"max_elevation":1700,"name":"MileHigh10k"}
        serializer = RouteSerializer(json)
        route = serializer.serialized

        self.assertEqual(route.id, 341663347)
        self.assertEqual(route.name, json['name'])
        self.assertEqual(route.description, json['description'])
        self.assertEqual(route.distance, json['distance'])
        self.assertTrue(isinstance(route.points(), (list, tuple)) and len(route.points()) == 3)
        self.assertTrue(isinstance(route.points(geojson=True), dict) and len(route.points(geojson=True)['coordinates']) == 3)
        self.assertEqual(route.ascent, 600)
        self.assertEqual(route.descent, 300)
        self.assertEqual(route.min_elevation, 1500)
        self.assertEqual(route.max_elevation, 1700)
        self.assertEqual(route.city, 'Littleton')
        self.assertEqual(route.state, 'CO')
        self.assertEqual(route.country, 'US')
        self.assertEqual(route.privacy, 'Private')
        self.assertEqual(route.created_datetime, iso_format_to_datetime(json['created_datetime']))
        self.assertEqual(route.updated_datetime, iso_format_to_datetime(json['updated_datetime']))
