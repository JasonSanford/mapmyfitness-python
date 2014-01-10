import httpretty

from mapmyfitness.serializers import WorkoutSerializer
from mapmyfitness.utils import iso_format_to_datetime

from tests import MapMyFitnessTestCase


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
