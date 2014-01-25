import datetime

import httpretty

from mapmyfitness.exceptions import InvalidSearchArgumentsException, AttributeNotFoundException, InvalidSizeException
from mapmyfitness.serializers import UserSerializer
from mapmyfitness.utils import iso_format_to_datetime

from tests import MapMyFitnessTestCase


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

    @httpretty.activate
    def test_get_profile_photo(self):
        uri_user = self.uri_root + '/user/9118466'
        uri_user_profile_photo = self.uri_root + '/user_profile_photo/9118466'

        content_returned_user = '{"username": "JasonSanford", "first_name": "Jason", "last_name": "Sanford", "display_name": "Jason Sanford", "last_initial": "S.", "weight": 91.17206637, "communication": {"promotions": true, "newsletter": true, "system_messages": true}, "display_measurement_system": "imperial", "time_zone": "America/Denver", "birthdate": "1983-04-15", "height": 1.778, "sharing": {"twitter": false, "facebook": false}, "last_login": "2014-01-16T03:43:16+00:00", "location": {"country": "US", "region": "CO", "address": "7910 S Bemis St", "locality": "Littleton"}, "gender": "M", "id": 9118466, "_links": {"stats": [{"href": "/v7.0/user_stats/9118466/?aggregate_by_period=month", "id": "9118466", "name": "month"}, {"href": "/v7.0/user_stats/9118466/?aggregate_by_period=year", "id": "9118466", "name": "year"}, {"href": "/v7.0/user_stats/9118466/?aggregate_by_period=day", "id": "9118466", "name": "day"}, {"href": "/v7.0/user_stats/9118466/?aggregate_by_period=week", "id": "9118466", "name": "week"}, {"href": "/v7.0/user_stats/9118466/?aggregate_by_period=lifetime", "id": "9118466", "name": "lifetime"}], "privacy": [{"href": "/v7.0/privacy_option/3/", "id": "3", "name": "profile"}, {"href": "/v7.0/privacy_option/3/", "id": "3", "name": "workout"}, {"href": "/v7.0/privacy_option/3/", "id": "3", "name": "activity_feed"}, {"href": "/v7.0/privacy_option/1/", "id": "1", "name": "food_log"}, {"href": "/v7.0/privacy_option/3/", "id": "3", "name": "email_search"}, {"href": "/v7.0/privacy_option/3/", "id": "3", "name": "route"}], "image": [{"href": "/v7.0/user_profile_photo/9118466/", "id": "9118466", "name": "user_profile_photo"}], "documentation": [{"href": "https://developer.mapmyapi.com/docs/User"}], "deactivation": [{"href": "/v7.0/user_deactivation/"}], "friendships": [{"href": "/v7.0/friendship/?from_user=9118466"}], "workouts": [{"href": "/v7.0/workout/?user=9118466&order_by=-start_datetime"}], "self": [{"href": "/v7.0/user/9118466/", "id": "9118466"}]}, "email": "jasonsanford@gmail.com", "date_joined": "2011-08-26T06:06:19+00:00"}'
        content_returned_user_profile_photo = '{"_links":{"small":[{"href":"http:\/\/isds-reader.mapmyfitness.com\/947c55cd-cb05-4a45-8b78-8af479c1da43\/Small"}],"large":[{"href":"http:\/\/isds-reader.mapmyfitness.com\/947c55cd-cb05-4a45-8b78-8af479c1da43\/Large"}],"self":[{"href":"\/v7.0\/user_profile_photo\/9118466\/","id":"9118466"}],"medium":[{"href":"http:\/\/isds-reader.mapmyfitness.com\/947c55cd-cb05-4a45-8b78-8af479c1da43\/Medium"}],"documentation":[{"href":"https:\/\/developer.mapmyapi.com\/docs\/User_Profile_Photos"}]}}'

        httpretty.register_uri(httpretty.GET, uri_user, body=content_returned_user, status=200)
        httpretty.register_uri(httpretty.GET, uri_user_profile_photo, body=content_returned_user_profile_photo, status=200)

        user = self.mmf.user.find(9118466)
        self.assertEqual(user.get_profile_photo(size='small'), 'http://isds-reader.mapmyfitness.com/947c55cd-cb05-4a45-8b78-8af479c1da43/Small')
        self.assertEqual(user.get_profile_photo(size='medium'), 'http://isds-reader.mapmyfitness.com/947c55cd-cb05-4a45-8b78-8af479c1da43/Medium')
        self.assertEqual(user.get_profile_photo(size='large'), 'http://isds-reader.mapmyfitness.com/947c55cd-cb05-4a45-8b78-8af479c1da43/Large')
        self.assertRaisesRegexp(InvalidSizeException,
                                'User get_profile_photo size must one of "small", "medium" or "large".',
                                user.get_profile_photo, **{'size': 'Ludicrous'})

    def test_search_no_params(self):
        self.assertRaisesRegexp(InvalidSearchArgumentsException,
                                'Either a friends_with, requested_friendship_with or suggested_friends_for argument must be passed to search for users.',
                                self.mmf.user.search)

    def test_search_bad_friends_with(self):
        self.assertRaisesRegexp(InvalidSearchArgumentsException,
                                'User friends_with must be of type int.',
                                self.mmf.user.search, **{'friends_with': 'lobster'})

    def test_search_bad_requested_friendship_with(self):
        self.assertRaisesRegexp(InvalidSearchArgumentsException,
                                'User requested_friendship_with must be of type int.',
                                self.mmf.user.search,
                                **{'requested_friendship_with': 'lobster'})

    def test_search_suggested_friends_for_no_extra_params(self):
        self.assertRaisesRegexp(InvalidSearchArgumentsException,
                                'User suggested_friends_source or suggested_friends_emails must exist when searching users via suggested_friends_for.',
                                self.mmf.user.search,
                                **{'suggested_friends_for': 9118466})

    def test_search_suggested_friends_for_bad_source(self):
        self.assertRaisesRegexp(InvalidSearchArgumentsException,
                                'User suggested_friends_source must be "facebook".',
                                self.mmf.user.search,
                                **{'suggested_friends_for': 9118466, 'suggested_friends_source': 'myspace'})

    def test_search_suggested_friends_for_empty_email(self):
        self.assertRaisesRegexp(InvalidSearchArgumentsException,
                                'User suggested_friends_emails must not be empty.',
                                self.mmf.user.search,
                                **{'suggested_friends_for': 9118466, 'suggested_friends_emails': ''})

    @httpretty.activate
    def test_search_friends_with(self):
        uri = self.uri_root + '/user/?friends_with=9118466'
        content_returned = '{"_embedded":{"user":[{"username":"adam.mcmanus","first_name":"Adam","last_name":"McManus","display_name":"Adam M.","last_initial":"M.","_links":{"image":[{"href":"/v7.0/user_profile_photo/1039389/","id":"1039389","name":"user_profile_photo"}],"self":[{"href":"/v7.0/user/1039389/","id":"1039389"}],"privacy":[{"href":"/v7.0/privacy_option/3/","id":"3","name":"profile"}]},"id":1039389},{"username":"Ahawks","first_name":"AJ","last_name":"Hawks","display_name":"AJ H.","last_initial":"H.","_links":{"image":[{"href":"/v7.0/user_profile_photo/1537259/","id":"1537259","name":"user_profile_photo"}],"self":[{"href":"/v7.0/user/1537259/","id":"1537259"}],"privacy":[{"href":"/v7.0/privacy_option/1/","id":"1","name":"profile"}]},"id":1537259}]},"_links":{"self":[{"href":"/v7.0/user/?limit=20&friends_with=9118466&offset=0"}],"documentation":[{"href":"https://developer.mapmyapi.com/docs/User"}],"next":[{"href":"/v7.0/user/?limit=20&friends_with=9118466&offset=20"}]},"total_count":52}'
        httpretty.register_uri(httpretty.GET, uri, body=content_returned, status=200)
        users = self.mmf.user.search(friends_with=9118466)
        self.assertEqual(len(users), 2)

    @httpretty.activate
    def test_search_friends_with_then_find_for_details(self):
        uri_search = self.uri_root + '/user/?friends_with=9118466'
        uri_find = self.uri_root + '/user/1039389'

        content_returned_search = '{"_embedded":{"user":[{"username":"adam.mcmanus","first_name":"Adam","last_name":"McManus","display_name":"Adam M.","last_initial":"M.","_links":{"image":[{"href":"/v7.0/user_profile_photo/1039389/","id":"1039389","name":"user_profile_photo"}],"self":[{"href":"/v7.0/user/1039389/","id":"1039389"}],"privacy":[{"href":"/v7.0/privacy_option/3/","id":"3","name":"profile"}]},"id":1039389},{"username":"Ahawks","first_name":"AJ","last_name":"Hawks","display_name":"AJ H.","last_initial":"H.","_links":{"image":[{"href":"/v7.0/user_profile_photo/1537259/","id":"1537259","name":"user_profile_photo"}],"self":[{"href":"/v7.0/user/1537259/","id":"1537259"}],"privacy":[{"href":"/v7.0/privacy_option/1/","id":"1","name":"profile"}]},"id":1537259}]},"_links":{"self":[{"href":"/v7.0/user/?limit=20&friends_with=9118466&offset=0"}],"documentation":[{"href":"https://developer.mapmyapi.com/docs/User"}],"next":[{"href":"/v7.0/user/?limit=20&friends_with=9118466&offset=20"}]},"total_count":52}'
        content_returned_find = '{"username": "adam.mcmanus", "first_name": "Adam", "last_name": "McManus", "display_name": "Adam McManus", "last_initial": "M.", "gender": "M", "time_zone": "America/Chicago", "_links": {"stats": [{"href": "/v7.0/user_stats/1039389/?aggregate_by_period=month", "id": "1039389", "name": "month"}, {"href": "/v7.0/user_stats/1039389/?aggregate_by_period=week", "id": "1039389", "name": "week"}, {"href": "/v7.0/user_stats/1039389/?aggregate_by_period=year", "id": "1039389", "name": "year"}, {"href": "/v7.0/user_stats/1039389/?aggregate_by_period=lifetime", "id": "1039389", "name": "lifetime"}, {"href": "/v7.0/user_stats/1039389/?aggregate_by_period=day", "id": "1039389", "name": "day"}], "privacy": [{"href": "/v7.0/privacy_option/3/", "id": "3", "name": "profile"}], "self": [{"href": "/v7.0/user/1039389/", "id": "1039389"}], "documentation": [{"href": "https://developer.mapmyapi.com/docs/User"}], "workouts": [{"href": "/v7.0/workout/?user=1039389&order_by=-start_datetime"}], "image": [{"href": "/v7.0/user_profile_photo/1039389/", "id": "1039389", "name": "user_profile_photo"}]}, "location": {"country": "US", "region": "TX", "locality": "Austin"}, "id": 1039389, "date_joined": "2009-01-14T21:35:50+00:00"}'

        httpretty.register_uri(httpretty.GET, uri_search, body=content_returned_search, status=200)
        httpretty.register_uri(httpretty.GET, uri_find, body=content_returned_find, status=200)

        users = self.mmf.user.search(friends_with=9118466)
        user = users[0]
        self.assertEqual(user.location['locality'], 'Austin')

    @httpretty.activate
    def test_search_friends_with_then_find_for_details_missing_property(self):
        uri_search = self.uri_root + '/user/?friends_with=9118466'
        uri_find = self.uri_root + '/user/1039389'

        content_returned_search = '{"_embedded":{"user":[{"username":"adam.mcmanus","first_name":"Adam","last_name":"McManus","display_name":"Adam M.","last_initial":"M.","_links":{"image":[{"href":"/v7.0/user_profile_photo/1039389/","id":"1039389","name":"user_profile_photo"}],"self":[{"href":"/v7.0/user/1039389/","id":"1039389"}],"privacy":[{"href":"/v7.0/privacy_option/3/","id":"3","name":"profile"}]},"id":1039389},{"username":"Ahawks","first_name":"AJ","last_name":"Hawks","display_name":"AJ H.","last_initial":"H.","_links":{"image":[{"href":"/v7.0/user_profile_photo/1537259/","id":"1537259","name":"user_profile_photo"}],"self":[{"href":"/v7.0/user/1537259/","id":"1537259"}],"privacy":[{"href":"/v7.0/privacy_option/1/","id":"1","name":"profile"}]},"id":1537259}]},"_links":{"self":[{"href":"/v7.0/user/?limit=20&friends_with=9118466&offset=0"}],"documentation":[{"href":"https://developer.mapmyapi.com/docs/User"}],"next":[{"href":"/v7.0/user/?limit=20&friends_with=9118466&offset=20"}]},"total_count":52}'
        content_returned_find = '{"username": "adam.mcmanus", "first_name": "Adam", "last_name": "McManus", "display_name": "Adam McManus", "last_initial": "M.", "gender": "M", "time_zone": "America/Chicago", "_links": {"stats": [{"href": "/v7.0/user_stats/1039389/?aggregate_by_period=month", "id": "1039389", "name": "month"}, {"href": "/v7.0/user_stats/1039389/?aggregate_by_period=week", "id": "1039389", "name": "week"}, {"href": "/v7.0/user_stats/1039389/?aggregate_by_period=year", "id": "1039389", "name": "year"}, {"href": "/v7.0/user_stats/1039389/?aggregate_by_period=lifetime", "id": "1039389", "name": "lifetime"}, {"href": "/v7.0/user_stats/1039389/?aggregate_by_period=day", "id": "1039389", "name": "day"}], "privacy": [{"href": "/v7.0/privacy_option/3/", "id": "3", "name": "profile"}], "self": [{"href": "/v7.0/user/1039389/", "id": "1039389"}], "documentation": [{"href": "https://developer.mapmyapi.com/docs/User"}], "workouts": [{"href": "/v7.0/workout/?user=1039389&order_by=-start_datetime"}], "image": [{"href": "/v7.0/user_profile_photo/1039389/", "id": "1039389", "name": "user_profile_photo"}]}, "location": {"country": "US", "region": "TX", "locality": "Austin"}, "id": 1039389, "date_joined": "2009-01-14T21:35:50+00:00"}'

        httpretty.register_uri(httpretty.GET, uri_search, body=content_returned_search, status=200)
        httpretty.register_uri(httpretty.GET, uri_find, body=content_returned_find, status=200)

        users = self.mmf.user.search(friends_with=9118466)
        user = users[0]
        self.assertEqual(user.location['locality'], 'Austin')
        self.assertRaises(AttributeNotFoundException, lambda: user.shoe_size)

    def test_serializer(self):
        user_json = {"username":"JasonSanford","first_name":"Jason","last_name":"Sanford","display_name":"Jason Sanford","last_initial":"S.","weight":91.17206637,"communication":{"promotions":True,"newsletter":True,"system_messages":True},"display_measurement_system":"imperial","time_zone":"America/Denver","birthdate":"1983-04-15","height":1.778,"sharing":{"twitter":False,"facebook":False},"last_login":"2014-01-16T03:43:16+00:00","location":{"country":"US","region":"CO","address":"7910 S BemisSt","locality":"Littleton"},"gender":"M","id":9118466,"_links":{"stats":[{"href":"/v7.0/user_stats/9118466/?aggregate_by_period=month","id":"9118466","name":"month"},{"href":"/v7.0/user_stats/9118466/?aggregate_by_period=year","id":"9118466","name":"year"},{"href":"/v7.0/user_stats/9118466/?aggregate_by_period=day","id":"9118466","name":"day"},{"href":"/v7.0/user_stats/9118466/?aggregate_by_period=week","id":"9118466","name":"week"},{"href":"/v7.0/user_stats/9118466/?aggregate_by_period=lifetime","id":"9118466","name":"lifetime"}],"privacy":[{"href":"/v7.0/privacy_option/3/","id":"3","name":"profile"},{"href":"/v7.0/privacy_option/3/","id":"3","name":"workout"},{"href":"/v7.0/privacy_option/3/","id":"3","name":"activity_feed"},{"href":"/v7.0/privacy_option/1/","id":"1","name":"food_log"},{"href":"/v7.0/privacy_option/3/","id":"3","name":"email_search"},{"href":"/v7.0/privacy_option/3/","id":"3","name":"route"}],"image":[{"href":"/v7.0/user_profile_photo/9118466/","id":"9118466","name":"user_profile_photo"}],"documentation":[{"href":"https://developer.mapmyapi.com/docs/User"}],"deactivation":[{"href":"/v7.0/user_deactivation/"}],"friendships":[{"href":"/v7.0/friendship/?from_user=9118466"}],"workouts":[{"href":"/v7.0/workout/?user=9118466&order_by=-start_datetime"}],"self":[{"href":"/v7.0/user/9118466/","id":"9118466"}]},"email":"jasonsanford@gmail.com","date_joined":"2011-08-26T06:06:19+00:00"}
        serializer = UserSerializer(user_json)
        user = serializer.serialized

        self.assertEqual(user.id, 9118466)
        self.assertEqual(user.username, 'JasonSanford')
        self.assertEqual(user.first_name, 'Jason')
        self.assertEqual(user.last_name, 'Sanford')
        self.assertEqual(user.email, 'jasonsanford@gmail.com')
        self.assertEqual(user.time_zone, 'America/Denver')
        self.assertEqual(user.birthdate, datetime.date(1983, 4, 15))
        self.assertEqual(user.display_measurement_system, user_json['display_measurement_system'])
        self.assertEqual(user.gender, 'M')
        self.assertEqual(user.height, 1.778)
        self.assertEqual(user.weight, 91.17206637)
        self.assertTrue('address' in user.location and 'locality' in user.location and 'region' in user.location and 'country' in user.location)
        self.assertEqual(user.join_datetime, iso_format_to_datetime(user_json['date_joined']))
