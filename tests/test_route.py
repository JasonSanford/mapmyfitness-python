import copy
import json

import httpretty

from mapmyfitness.constants import PUBLIC
from mapmyfitness.exceptions import InvalidSearchArgumentsException, InvalidObjectException, ValidatorException, InternalServerErrorException, BadRequestException, UnauthorizedException
from mapmyfitness.objects.route import RouteObject
from mapmyfitness.serializers import RouteSerializer
from mapmyfitness.utils import iso_format_to_datetime
from mapmyfitness.validators.route import RouteValidator

from tests import MapMyFitnessTestCase, MapMyFitnessTestCaseCacheFinds
from tests.valid_objects import route as valid_route


class RouteTestCacheFinds(MapMyFitnessTestCaseCacheFinds):
    @httpretty.activate
    def test_find(self):
        uri = self.uri_root + '/route/342208467'
        content_returned = '{"total_descent": null, "city": "Denver", "data_source": "run:RE", "description": "", "updated_datetime": "2014-01-06T22:26:50+00:00", "created_datetime": "2014-01-06T23:26:18+00:00", "country": "us", "start_point_type": "", "starting_location": {"type": "Point", "coordinates": [-104.99652, 39.7499]}, "points": null, "name": "Tuesday Lunch Run", "climbs": null, "state": "CO", "max_elevation": null, "postal_code": "80202", "min_elevation": null, "total_ascent": null, "_links": {"activity_types": [{"href": "/v7.0/activity_type/16/", "id": "16"}], "privacy": [{"href": "/v7.0/privacy_option/0/", "id": "0"}], "self": [{"href": "/v7.0/route/342208467/", "id": "342208467"}], "alternate": [{"href": "/v7.0/route/342208467/?format=kml&field_set=detailed", "id": "342208467", "name": "kml"}], "user": [{"href": "/v7.0/user/1/", "id": "1"}], "thumbnail": [{"href": "//images.mapmycdn.com/routes/thumbnail/342208467?size=100x100"}], "documentation": [{"href": "https://developer.mapmyapi.com/docs/Route"}]}, "distance": 5506.3582910718}'
        httpretty.register_uri(httpretty.GET, uri, body=content_returned, status=200)
        route = self.mmf.route.find(342208467)
        self.assertEqual(route.id, 342208467)

        route_again = self.mmf.route.find(342208467)
        self.assertEqual(route_again.id, 342208467)

class RouteTest(MapMyFitnessTestCase):
    def test_validator_bad_kwargs(self):
        self.assertRaises(ValidatorException, RouteValidator)

    def test_no_filter(self):
        self.assertRaisesRegexp(InvalidSearchArgumentsException,
                                'Either a user, users or close_to_location argument must be passed to search for routes.',
                                self.mmf.route.search)

    def test_create_no_name(self):
        a_route = copy.deepcopy(valid_route)
        del a_route['name']
        self.assertRaisesRegexp(InvalidObjectException,
                                'Route name must exist and be of type str.',
                                self.mmf.route.create, a_route)

    def test_create_no_distance(self):
        a_route = copy.deepcopy(valid_route)
        del a_route['distance']
        self.assertRaisesRegexp(InvalidObjectException,
                                'Route distance must exist and be of type int or float.',
                                self.mmf.route.create, a_route)

    def test_create_no_privacy(self):
        a_route = copy.deepcopy(valid_route)
        del a_route['privacy']
        self.assertRaisesRegexp(InvalidObjectException,
                                'Route privacy must exist and be one of constants.PUBLIC, constants.PRIVATE or constants.FRIENDS.',
                                self.mmf.route.create, a_route)

    def test_create_bad_point(self):
        a_route = copy.deepcopy(valid_route)
        a_route['points'][0] = 'lobster'
        self.assertRaisesRegexp(InvalidObjectException,
                                'Each point in Route points must be of type dict.',
                                self.mmf.route.create, a_route)

    def test_create_bad_point_lat(self):
        a_route = copy.deepcopy(valid_route)
        a_route['points'][0]['lng'] = 'lobster'
        self.assertRaisesRegexp(InvalidObjectException,
                                'Each point in Route points must have a "lng" key and be of type int or float.',
                                self.mmf.route.create, a_route)

    def test_all_bad_user(self):
        self.assertRaisesRegexp(InvalidSearchArgumentsException,
                                'Route user must be of type int.',
                                self.mmf.route.search, **{'user':'lobster'})

    def test_all_bad_users_not_list(self):
        self.assertRaisesRegexp(InvalidSearchArgumentsException,
                                'Route users must be a list or tuple of ints.',
                                self.mmf.route.search, **{'users': 'lobsters'})

    def test_all_bad_users_not_ints(self):
        self.assertRaisesRegexp(InvalidSearchArgumentsException,
                                'Route users must be a list or tuple of ints.',
                                self.mmf.route.search, **{'users':(9118466, 'lobster')})

    @httpretty.activate
    def test_all_user_success(self):
        uri = self.uri_root + '/route/?field_set=detailed&user=9118466'
        content_returned = '{"_embedded": {"routes": [{"total_descent": -9.8980420904, "city": "Boston", "data_source": "MapMyRide", "description": "Easy and Quick daily run from Downtown Crossing", "updated_datetime": "2006-09-18T18:12:19+00:00", "created_datetime": "2006-09-18T18:12:19+00:00", "country": "us", "start_point_type": "", "starting_location": {"type": "Point", "coordinates": [-71.0617160797, 42.3561337597]}, "distance": 7998.43968, "total_ascent": 0.0, "climbs": [], "state": "MA", "points": [{"lat": 42.3561337597, "lng": -71.0617160797, "dis": 0.0, "ele": 30.28}, {"lat": 42.3562606124, "lng": -71.0616731644, "dis": 14.53, "ele": 30.5}], "postal_code": "02108", "min_elevation": 4.43, "_links": {"activity_types": [{"href": "/v7.0/activity_type/16/", "id": "16"}], "privacy": [{"href": "/v7.0/privacy_option/3/", "id": "3"}], "self": [{"href": "/v7.0/route/128262/", "id": "128262"}], "alternate": [{"href": "/v7.0/route/128262/?format=kml&field_set=detailed", "id": "128262", "name": "kml"}], "user": [{"href": "/v7.0/user/36142/", "id": "36142"}], "thumbnail": [{"href": "//images.mapmycdn.com/routes/thumbnail/128262?size=100x100"}]}, "max_elevation": 31.81, "name": "Regular Run 1"}]}}'
        httpretty.register_uri(httpretty.GET, uri, body=content_returned, status=200)
        routes = self.mmf.route.search(user=9118466)
        self.assertIsInstance(routes, list)
        self.assertIsInstance(routes[0], RouteObject)

    def test_all_close_to_location_latlng_not_list(self):
        self.assertRaisesRegexp(InvalidSearchArgumentsException,
                                'Route close_to_location must be a list or 2-tuple of latitude,longitude.',
                                self.mmf.route.search, **{'close_to_location':'lobsters'})

    def test_all_close_to_location_latlng_not_floatable(self):
        self.assertRaisesRegexp(InvalidSearchArgumentsException,
                                'Route close_to_location must be a list or 2-tuple of latitude,longitude.',
                                self.mmf.route.search, **{'close_to_location': (40.732, 'lobster')})

    def test_all_close_to_location_bad_distance(self):
        self.assertRaisesRegexp(InvalidSearchArgumentsException,
                                'Route minimum_distance must be of type int or float.',
                                self.mmf.route.search,
                                **{'close_to_location': (40.732, -105), 'minimum_distance': 'lobster'})

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
    def test_500(self):
        uri = self.uri_root + '/route/342208467'
        content_returned = '{"error": "yep"}'
        httpretty.register_uri(httpretty.GET, uri, body=content_returned, status=500)
        self.assertRaises(InternalServerErrorException, self.mmf.route.find,
                          342208467)

    @httpretty.activate
    def test_400(self):
        uri = self.uri_root + '/route/?field_set=detailed'
        content_returned = '{"_diagnostics": {"validation_failures": [{"points": ["This field is required."]}]}, "_links": {"self": [{"href": "/v7.0/route/?limit=20&offset=0"}], "documentation": [{"href": "https://developer.mapmyapi.com/docs/Route"}]}}'
        httpretty.register_uri(httpretty.POST, uri, body=content_returned, status=400)
        self.assertRaisesRegexp(BadRequestException,
                                'points This field is required.',
                                self.mmf.route.create, valid_route)

    @httpretty.activate
    def test_401(self):
        uri = self.uri_root + '/route/?field_set=detailed&user=9118466'
        content_returned = '{"oauth1_error": "Malformed authorization header", "oauth1_error_code": "OAUTH1:UNKNOWN", "oauth2_error": "AccessToken not found.", "oauth2_error_code": "OAUTH2:ACCESSTOKEN_NOT_FOUND"}'
        httpretty.register_uri(httpretty.GET, uri, body=content_returned, status=401)
        self.assertRaises(UnauthorizedException,
                          self.mmf.route.search, **{'user': 9118466})

    @httpretty.activate
    def test_update(self):
        uri = self.uri_root + '/route/342208467/'
        update_with = {"privacy": PUBLIC, "total_descent": None, "city": "Denver", "data_source": "run:RE", "description": "Now you have a description.", "updated_datetime": "2014-01-06T22:26:50+00:00", "created_datetime": "2014-01-06T23:26:18+00:00", "country": "us", "start_point_type": "", "starting_location": {"type": "Point", "coordinates": [-104.99652, 39.7499]}, "points": [{"lat":39.5735,"lng":-105.0164},{"lat":39.6781,"lng":-104.9926},{"lat":39.75009,"lng":-104.99656}], "name": "Tuesday Lunch Run", "climbs": None, "state": "CO", "max_elevation": None, "postal_code": "80202", "min_elevation": None, "total_ascent": None, "_links": {"activity_types": [{"href": "/v7.0/activity_type/16/", "id": "16"}], "privacy": [{"href": "/v7.0/privacy_option/0/", "id": "0"}], "self": [{"href": "/v7.0/route/342208467/", "id": "342208467"}], "alternate": [{"href": "/v7.0/route/342208467/?format=kml&field_set=detailed", "id": "342208467", "name": "kml"}], "user": [{"href": "/v7.0/user/1/", "id": "1"}], "thumbnail": [{"href": "//images.mapmycdn.com/routes/thumbnail/342208467?size=100x100"}], "documentation": [{"href": "https://developer.mapmyapi.com/docs/Route"}]}, "distance": 5506.3582910718}
        content_returned = json.dumps(update_with)
        httpretty.register_uri(httpretty.PUT, uri, body=content_returned, status=200)
        route = self.mmf.route.update(342208467, update_with)
        self.assertEqual(route.description, 'Now you have a description.')

    def test_update_no_privacy(self):
        update_with = {"privacy": PUBLIC, "total_descent": None, "city": "Denver", "data_source": "run:RE", "description": "Now you have a description.", "updated_datetime": "2014-01-06T22:26:50+00:00", "created_datetime": "2014-01-06T23:26:18+00:00", "country": "us", "start_point_type": "", "starting_location": {"type": "Point", "coordinates": [-104.99652, 39.7499]}, "points": [{"lat":39.5735,"lng":-105.0164},{"lat":39.6781,"lng":-104.9926},{"lat":39.75009,"lng":-104.99656}], "name": "Tuesday Lunch Run", "climbs": None, "state": "CO", "max_elevation": None, "postal_code": "80202", "min_elevation": None, "total_ascent": None, "_links": {"activity_types": [{"href": "/v7.0/activity_type/16/", "id": "16"}], "privacy": [{"href": "/v7.0/privacy_option/0/", "id": "0"}], "self": [{"href": "/v7.0/route/342208467/", "id": "342208467"}], "alternate": [{"href": "/v7.0/route/342208467/?format=kml&field_set=detailed", "id": "342208467", "name": "kml"}], "user": [{"href": "/v7.0/user/1/", "id": "1"}], "thumbnail": [{"href": "//images.mapmycdn.com/routes/thumbnail/342208467?size=100x100"}], "documentation": [{"href": "https://developer.mapmyapi.com/docs/Route"}]}, "distance": 5506.3582910718}
        del update_with['privacy']
        self.assertRaisesRegexp(InvalidObjectException,
                                'Route privacy must exist and be one of constants.PUBLIC, constants.PRIVATE or constants.FRIENDS.',
                                self.mmf.route.update, 342208467, update_with)

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
