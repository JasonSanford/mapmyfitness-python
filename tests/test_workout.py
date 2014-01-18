import copy
import datetime

import httpretty

from mapmyfitness.exceptions import BadRequestException, InvalidObjectException, InvalidSearchArgumentsException
from mapmyfitness.objects.workout import WorkoutObject
from mapmyfitness.serializers import WorkoutSerializer
from mapmyfitness.utils import iso_format_to_datetime

from tests import MapMyFitnessTestCase
from tests.valid_objects import workout as valid_workout


class WorkoutTest(MapMyFitnessTestCase):
    @httpretty.activate
    def test_find_with_route(self):
        uri = self.uri_root + '/workout/93093928'
        content_returned = '{"start_locale_timezone": "America/Denver", "source": "UnknownFile(http://ridewithgps.com/:gpx)", "start_datetime": "2011-06-22T15:27:00+00:00", "_links": {"self": [{"href": "/v7.0/workout/93093928/", "id": "93093928"}], "route": [{"href": "/v7.0/route/68443498/", "id": "68443498"}], "activity_type": [{"href": "/v7.0/activity_type/11/", "id": "11"}], "user": [{"href": "/v7.0/user/9118466/", "id": "9118466"}], "privacy": [{"href": "/v7.0/privacy_option/1/", "id": "1"}]}, "name": "Bike to Work Day - return", "updated_datetime": "2012-02-09T19:15:38+00:00", "created_datetime": "2012-02-09T19:14:43+00:00", "aggregates": {"active_time_total": 4119, "distance_total": 20985.84576, "speed_max": 25.179483296000001, "steps_total": 0, "speed_avg": 5.0948701759999997, "elapsed_time_total": 4080, "metabolic_energy_total": 2422536}, "has_time_series": true, "reference_key": "2011-06-2215:27:08+00:00"}'
        httpretty.register_uri(httpretty.GET, uri, body=content_returned, status=200)
        workout = self.mmf.workout.find(93093928)
        self.assertEqual(workout.id, 93093928)
        self.assertEqual(workout.route_id, 68443498)

    @httpretty.activate
    def test_find_no_route(self):
        uri = self.uri_root + '/workout/459272681'
        content_returned = '{"start_locale_timezone": "America/Denver", "source": null, "start_datetime": "2014-01-09T23:28:37+00:00", "_links": {"self": [{"href": "/v7.0/workout/459272681/", "id": "459272681"}], "documentation": [{"href": "https://developer.mapmyapi.com/docs/Workout"}], "activity_type": [{"href": "/v7.0/activity_type/321/", "id": "321"}], "user": [{"href": "/v7.0/user/9118466/", "id": "9118466"}], "privacy": [{"href": "/v7.0/privacy_option/3/", "id": "3"}]}, "name": "Walked to Candy", "updated_datetime": "2014-01-09T22:30:07+00:00", "created_datetime": "2014-01-09T22:30:07+00:00", "aggregates": {"active_time_total": 90.0, "elapsed_time_total": 90, "distance_total": 0.0, "metabolic_energy_total": 66944.0, "steps_total": 0.0}, "has_time_series": false, "reference_key": null}'
        httpretty.register_uri(httpretty.GET, uri, body=content_returned, status=200)
        workout = self.mmf.workout.find(459272681)
        self.assertEqual(workout.id, 459272681)
        self.assertIsNone(workout.route_id)
        self.assertIsNone(workout.speed_avg)

    @httpretty.activate
    def test_create_bad_request_validation_errors(self):
        uri = self.uri_root + '/workout/'
        content_returned = '{"_diagnostics":{"validation_failures":[["user filter required"]]},"_links":{"self":[{"href":"\/v7.0\/workout\/?limit=20&offset=0"}],"documentation":[{"href":"https:\/\/developer.mapmyapi.com\/docs\/Workout"}]}}'
        httpretty.register_uri(httpretty.POST, uri, body=content_returned, status=400)
        try:
            self.mmf.workout.create(valid_workout)
        except Exception as exc:
            self.assertIsInstance(exc, BadRequestException)
            self.assertEqual(str(exc), 'user filter required.')

    @httpretty.activate
    def test_create_success(self):
        a_workout = copy.deepcopy(valid_workout)
        uri = self.uri_root + '/workout/'
        content_returned = '{"start_datetime":"2014-01-09T10:08:07+00:00","name":"Test workout via API","updated_datetime":"2014-01-11T06:57:10+00:00","created_datetime":"2014-01-11T06:57:10+00:00","aggregates":{"active_time_total":600.0,"elapsed_time_total":650,"distance_total":0.0},"reference_key":null,"start_locale_timezone":"America\/Denver","source":"","_links":{"documentation":[{"href":"https:\/\/developer.mapmyapi.com\/docs\/Workout"}],"self":[{"href":"\/v7.0\/workout\/460043307\/","id":"460043307"}],"activity_type":[{"href":"\/v7.0\/activity_type\/11\/","id":"11"}],"user":[{"href":"\/v7.0\/user\/14122640\/","id":"14122640"}],"privacy":[{"href":"\/v7.0\/privacy_option\/1\/","id":"1"}]},"has_time_series":false}'
        httpretty.register_uri(httpretty.POST, uri, body=content_returned, status=201)
        w = self.mmf.workout.create(a_workout)
        self.assertIsInstance(w, WorkoutObject)
        self.assertEqual(w.id, 460043307)

    def test_create_no_activity_type(self):
        a_workout = copy.deepcopy(valid_workout)
        del a_workout['activity_type']
        try:
            self.mmf.workout.create(a_workout)
        except Exception as exc:
            self.assertIsInstance(exc, InvalidObjectException)
            self.assertEqual(str(exc), 'Workout activity_type must exist and be of type int.')

    def test_create_no_start_datetime(self):
        a_workout = copy.deepcopy(valid_workout)
        del a_workout['start_datetime']
        try:
            self.mmf.workout.create(a_workout)
        except Exception as exc:
            self.assertIsInstance(exc, InvalidObjectException)
            self.assertEqual(str(exc), 'Workout start_datetime must exist and be of type datetime.datetime.')

    def test_create_bad_aggregate(self):
        a_workout = copy.deepcopy(valid_workout)
        a_workout['active_time_total'] = 'lobster'
        try:
            self.mmf.workout.create(a_workout)
        except Exception as exc:
            self.assertIsInstance(exc, InvalidObjectException)
            self.assertEqual(str(exc), 'Workout active_time_total must be of type int or float.')

    def test_create_bad_position(self):
        a_workout = copy.deepcopy(valid_workout)
        a_workout['time_series']['position'][0].append('lobster')
        try:
            self.mmf.workout.create(a_workout)
        except Exception as exc:
            self.assertIsInstance(exc, InvalidObjectException)
            self.assertEqual(str(exc), 'Workout time_series position must be a 2-list with the first item being of type int or float and the second item being a dict.')

    def test_create_missing_lat(self):
        a_workout = copy.deepcopy(valid_workout)
        del a_workout['time_series']['position'][0][1]['lat']
        try:
            self.mmf.workout.create(a_workout)
        except Exception as exc:
            self.assertIsInstance(exc, InvalidObjectException)
            self.assertEqual(str(exc), 'Workout time_series position dict must have a lat key and be of type int or float.')

    def test_create_bad_time_series(self):
        a_workout = copy.deepcopy(valid_workout)
        a_workout['time_series']['heartrate'][0].append('lobster')
        try:
            self.mmf.workout.create(a_workout)
        except Exception as exc:
            self.assertIsInstance(exc, InvalidObjectException)
            self.assertEqual(str(exc), 'Workout time_series heartrate must be a 2-list with each item being of type int or float.')

    def test_search_no_user(self):
        try:
            self.mmf.workout.search()
        except Exception as exc:
            self.assertIsInstance(exc, InvalidSearchArgumentsException)
            self.assertEqual(str(exc), 'Workout user must exist and be of type int.')

    def test_search_bad_date(self):
        try:
            self.mmf.workout.search(user=1234, created_after='not_a_date')
        except Exception as exc:
            self.assertIsInstance(exc, InvalidSearchArgumentsException)
            self.assertEqual(str(exc), 'Workout created_after must be of type datetime.datetime.')

    def test_search_bad_activity_type(self):
        try:
            self.mmf.workout.search(user=1234, activity_type='lobster')
        except Exception as exc:
            self.assertIsInstance(exc, InvalidSearchArgumentsException)
            self.assertEqual(str(exc), 'Workout activity_type must be of type int.')

    @httpretty.activate
    def test_search_then_time_series(self):
        search_content_returned = '{"_embedded": {"workouts": [{"start_datetime": "2014-01-09T19:11:43+00:00", "name": "Ran 3.98 mi on 1/9/14", "updated_datetime": "2014-01-09T19:45:24+00:00", "created_datetime": "2014-01-09T19:45:24+00:00", "aggregates": {"active_time_total": 1963.0, "distance_total": 6410.12980608, "speed_max": 7.063053184, "steps_total": 0.0, "speed_avg": 3.2654439136, "elapsed_time_total": 1998, "metabolic_energy_total": 3091976.0}, "reference_key": null, "start_locale_timezone": "America/Denver", "source": "Mobile_Internal_RidePlus", "_links": {"user": [{"href": "/v7.0/user/9118466/", "id": "9118466"}], "route": [{"href": "/v7.0/route/343207741/", "id": "343207741"}], "privacy": [{"href": "/v7.0/privacy_option/3/", "id": "3"}], "self": [{"href": "/v7.0/workout/459164951/", "id": "459164951"}], "activity_type": [{"href": "/v7.0/activity_type/16/", "id": "16"}]}, "has_time_series": true}]}, "_links": {"self": [{"href": "/v7.0/workout/?started_after=2014-01-09T10%3A00%3A00%2B00%3A00&offset=0&limit=20&user=9118466&started_before=2014-01-09T11%3A00%3A00%2B00%3A00"}], "documentation": [{"href": "https://developer.mapmyapi.com/docs/Workout"}]}, "total_count": 1}'
        find_content_returned = '{"reference_key":null,"name":"Ran 3.98 mi on 1/9/14","updated_datetime":"2014-01-09T19:45:24+00:00","created_datetime":"2014-01-09T19:45:24+00:00","aggregates":{"active_time_total":1963,"distance_total":6410.12980608,"speed_max":7.063053184,"steps_total":0,"speed_avg":3.2654439136,"elapsed_time_total":1998,"metabolic_energy_total":3091976},"time_series":{"distance":[[3,2.000414592],[13,37.999830528000004],[23,121.000137984],[33,188.00034739199998],[43,244.00069056],[53,295.00080192],[63,339.00026688],[73,358.000182144],[83,447.000124032],[93,528.9994195200001],[103,597.0006408959999],[113,675.000716544],[123,748.999963008],[133,810.9999406080001],[143,857.9992227840002],[162,878.0001500160001],[172,958.000640256],[182,1004.9999224319998],[192,1013.99937408],[202,1031.0004840959998],[212,1064.99948544],[222,1169.999525376],[232,1169.999525376],[242,1169.999525376]],"heartrate":[[0,1.7833333333333332],[10,1.9],[20,1.9166666666666667],[30,1.9333333333333333],[40,1.65],[50,1.8333333333333333],[60,1.7166666666666666],[70,1.5666666666666667],[80,1.8],[90,1.8],[100,1.9666666666666666],[110,2.1666666666666665],[120,2.3666666666666667],[130,2.216666666666667],[140,2.1333333333333333],[159,2.0833333333333335],[169,2.1333333333333333],[179,1.9833333333333334],[189,2.05],[199,2.0833333333333335],[209,2.0166666666666666],[219,1.95],[229,2],[239,1.7166666666666666]],"speed":[[0,2.05555563488],[10,4.08333354528],[20,5.083333414720001],[30,4.861111171840001],[40,5.472222004480001],[50,4.916666620800001],[60,7.416666741439999],[70,5.777777867840001],[80,4.555555755520001],[90,6.277777802560001],[100,8.61111112928],[110,8.777777923200002],[120,6.250000078080001],[130,4.777777998400001],[140,6.416666872000001],[159,2.0000001859200003],[169,7.805555331199999],[179,8.0555557456],[189,7.055555429120001],[199,6.500000045440001],[209,4.527777584000001],[219,4.361111237120001],[229,4.361111237120001],[239,4.361111237120001]],"power":[[0,260],[10,190],[20,133],[30,105],[40,620],[50,3],[60,0],[70,0],[80,205],[90,235],[100,230],[110,446],[120,199],[130,0],[140,16],[159,128],[169,166],[179,0],[189,153],[199,128],[209,118],[219,108],[229,266],[239,0]],"position":[[0,{"lat":30.264079,"lng":-97.756105,"elevation":114.0000002952}],[10,{"lat":30.264757,"lng":-97.756513,"elevation":115.0000003272}],[20,{"lat":30.265158,"lng":-97.756079,"elevation":116.0000000544}],[30,{"lat":30.265543,"lng":-97.755788,"elevation":117.00000008640001}],[40,{"lat":30.266004,"lng":-97.755518,"elevation":118.0000001184}],[50,{"lat":30.266444,"lng":-97.755342,"elevation":118.0000001184}],[60,{"lat":30.267012,"lng":-97.754997,"elevation":117.00000008640001}],[70,{"lat":30.267411,"lng":-97.754984,"elevation":116.0000000544}],[80,{"lat":30.267664,"lng":-97.755526,"elevation":115.0000003272}],[90,{"lat":30.268191,"lng":-97.755392,"elevation":116.0000000544}],[100,{"lat":30.268929,"lng":-97.755139,"elevation":116.0000000544}],[110,{"lat":30.269647,"lng":-97.754832,"elevation":116.0000000544}],[120,{"lat":30.27017,"lng":-97.754546,"elevation":119.0000001504}],[130,{"lat":30.270107,"lng":-97.754024,"elevation":122.00000024639999}],[140,{"lat":30.269937,"lng":-97.753393,"elevation":122.00000024639999}],[159,{"lat":30.269897,"lng":-97.753218,"elevation":121.00000021439999}],[169,{"lat":30.269716,"lng":-97.752449,"elevation":120.0000001824}],[179,{"lat":30.269581,"lng":-97.75183,"elevation":120.0000001824}],[189,{"lat":30.269493,"lng":-97.751104,"elevation":119.0000001504}],[199,{"lat":30.269504,"lng":-97.75102,"elevation":119.0000001504}],[209,{"lat":30.269233,"lng":-97.749821,"elevation":120.0000001824}],[219,{"lat":30.268977,"lng":-97.749537,"elevation":120.0000001824}],[229,{"lat":30.268977,"lng":-97.749537,"elevation":120.0000001824}],[239,{"lat":30.268977,"lng":-97.749537,"elevation":120.0000001824}]]},"start_locale_timezone":"America/Denver","source":"Mobile_Internal_RidePlus","_links":{"privacy":[{"href":"/v7.0/privacy_option/3/","id":"3"}],"route":[{"href":"/v7.0/route/343207741/","id":"343207741"}],"documentation":[{"href":"https://developer.mapmyapi.com/docs/Workout"}],"user":[{"href":"/v7.0/user/9118466/","id":"9118466"}],"self":[{"href":"/v7.0/workout/459164951/?field_set=time_series","id":"459164951"}],"activity_type":[{"href":"/v7.0/activity_type/16/","id":"16"}]},"start_datetime":"2014-01-09T19:11:43+00:00","has_time_series":true}'

        uri_search = self.uri_root + '/workout/?started_after=2014-01-09T10%3A00%3A00%2B00%3A00&user=9118466&started_before=2014-01-09T11%3A00%3A00%2B00%3A00'
        uri_find = self.uri_root + '/workout/459164951?field_set=time_series'

        httpretty.register_uri(httpretty.GET, uri_search, body=search_content_returned, status=200)
        httpretty.register_uri(httpretty.GET, uri_find, body=find_content_returned, status=200)

        dt = datetime.datetime(2014, 1, 9, 10, 0, 0)
        dt2 = datetime.datetime(2014, 1, 9, 11, 0, 0)

        workouts = self.mmf.workout.search(user=9118466, started_after=dt, started_before=dt2)
        workout = workouts[0]
        time_series = workout.time_series
        time_series_again = workout.time_series  # Get the time_series from the _time_series attr

        self.assertTrue('distance' in time_series)
        self.assertTrue('power' in time_series)
        self.assertTrue('position' in time_series)

        self.assertTrue('distance' in time_series_again)

    def test_serializer(self):
        json = {'start_datetime': '2011-06-22T15:27:00+00:00', 'name': 'Bike to Work Day - return', 'updated_datetime': '2012-02-09T19:15:38+00:00', 'created_datetime': '2012-02-09T19:14:43+00:00', 'aggregates': {'active_time_total': 4119, 'distance_total': 20985.84576, 'speed_max': 25.179483296000001, 'steps_total': 0, 'speed_avg': 5.0948701759999997, 'elapsed_time_total': 4080, 'metabolic_energy_total': 2422536}, 'reference_key': '2011-06-2215:27:08+00:00', 'start_locale_timezone': "'murica/Denver", 'source': 'UnknownFile(http://ridewithgps.com/:gpx)', '_links': {'user': [{'href': '/v7.0/user/9118466/', 'id': '9118466'}], 'self': [{'href': '/v7.0/workout/93093928/', 'id': '93093928'}], 'privacy': [{'href': '/v7.0/privacy_option/1/', 'id': '1'}], 'route': [{'href': '/v7.0/route/68443498/', 'id': '68443498'}], 'activity_type': [{'href': '/v7.0/activity_type/11/', 'id': '11'}]}, 'has_time_series': True}
        serializer = WorkoutSerializer(json)
        workout = serializer.serialized

        self.assertEqual(workout.id, 93093928)
        self.assertEqual(workout.name, 'Bike to Work Day - return')
        self.assertEqual(workout.start_datetime, iso_format_to_datetime(json['start_datetime']))
        self.assertEqual(workout.created_datetime, iso_format_to_datetime(json['created_datetime']))
        self.assertEqual(workout.updated_datetime, iso_format_to_datetime(json['updated_datetime']))
        self.assertEqual(workout.start_locale_timezone, "'murica/Denver")
        self.assertEqual(workout.source, 'UnknownFile(http://ridewithgps.com/:gpx)')
        self.assertEqual(workout.active_time_total, 4119)
        self.assertEqual(workout.distance_total, 20985.84576)
        self.assertEqual(workout.steps_total, 0)
        self.assertEqual(workout.elapsed_time_total, 4080)
        self.assertEqual(workout.metabolic_energy_total, 2422536)
        self.assertEqual(workout.speed_max, 25.179483296000001)
        self.assertEqual(workout.speed_avg, 5.0948701759999997)
        self.assertEqual(workout.activity_type_id, 11)
        self.assertEqual(workout.privacy, 'Friends')
        self.assertTrue(workout.has_time_series)
