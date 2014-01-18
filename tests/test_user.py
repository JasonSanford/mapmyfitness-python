import copy

import httpretty

from mapmyfitness.exceptions import BadRequestException, InvalidObjectException, InvalidSearchArgumentsException
from mapmyfitness.objects.user import UserObject
from mapmyfitness.serializers import UserSerializer

from tests import MapMyFitnessTestCase
#from tests.valid_objects import user as valid_user


class UserTest(MapMyFitnessTestCase):
    def test_cannot_delete(self):
        try:
            self.mmf.user.delete(1234)
        except Exception as exc:
            self.assertIsInstance(exc, AttributeError)
            self.assertEqual(str(exc), "'User' object has no attribute 'delete'")


    def test_cannot_create(self):
        try:
            self.mmf.user.create(1234)
        except Exception as exc:
            self.assertIsInstance(exc, AttributeError)
            self.assertEqual(str(exc), "'User' object has no attribute 'create'")


    def test_cannot_update(self):
        try:
            self.mmf.user.update(1234)
        except Exception as exc:
            self.assertIsInstance(exc, AttributeError)
            self.assertEqual(str(exc), "'User' object has no attribute 'update'")

    @httpretty.activate
    def test_find(self):
        uri = self.uri_root + '/user/9118466'
        content_returned = '{"username": "JasonSanford", "first_name": "Jason", "last_name": "Sanford", "display_name": "Jason Sanford", "last_initial": "S.", "weight": 91.17206637, "communication": {"promotions": true, "newsletter": true, "system_messages": true}, "display_measurement_system": "imperial", "time_zone": "America/Denver", "birthdate": "1983-04-15", "height": 1.778, "sharing": {"twitter": false, "facebook": false}, "last_login": "2014-01-16T03:43:16+00:00", "location": {"country": "US", "region": "CO", "address": "7910 S Bemis St", "locality": "Littleton"}, "gender": "M", "id": 9118466, "_links": {"stats": [{"href": "/v7.0/user_stats/9118466/?aggregate_by_period=month", "id": "9118466", "name": "month"}, {"href": "/v7.0/user_stats/9118466/?aggregate_by_period=year", "id": "9118466", "name": "year"}, {"href": "/v7.0/user_stats/9118466/?aggregate_by_period=day", "id": "9118466", "name": "day"}, {"href": "/v7.0/user_stats/9118466/?aggregate_by_period=week", "id": "9118466", "name": "week"}, {"href": "/v7.0/user_stats/9118466/?aggregate_by_period=lifetime", "id": "9118466", "name": "lifetime"}], "privacy": [{"href": "/v7.0/privacy_option/3/", "id": "3", "name": "profile"}, {"href": "/v7.0/privacy_option/3/", "id": "3", "name": "workout"}, {"href": "/v7.0/privacy_option/3/", "id": "3", "name": "activity_feed"}, {"href": "/v7.0/privacy_option/1/", "id": "1", "name": "food_log"}, {"href": "/v7.0/privacy_option/3/", "id": "3", "name": "email_search"}, {"href": "/v7.0/privacy_option/3/", "id": "3", "name": "route"}], "image": [{"href": "/v7.0/user_profile_photo/9118466/", "id": "9118466", "name": "user_profile_photo"}], "documentation": [{"href": "https://developer.mapmyapi.com/docs/User"}], "deactivation": [{"href": "/v7.0/user_deactivation/"}], "friendships": [{"href": "/v7.0/friendship/?from_user=9118466"}], "workouts": [{"href": "/v7.0/workout/?user=9118466&order_by=-start_datetime"}], "self": [{"href": "/v7.0/user/9118466/", "id": "9118466"}]}, "email": "jasonsanford@gmail.com", "date_joined": "2011-08-26T06:06:19+00:00"}'
        httpretty.register_uri(httpretty.GET, uri, body=content_returned, status=200)
        user = self.mmf.user.find(9118466)
        self.assertEqual(user.id, 9118466)
