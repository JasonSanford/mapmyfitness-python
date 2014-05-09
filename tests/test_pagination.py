import datetime

import httpretty

from mapmyfitness.exceptions import PageNotAnInteger, EmptyPage
from mapmyfitness.objects.workout import WorkoutObject

from tests import MapMyFitnessTestCase


class PaginationTest(MapMyFitnessTestCase):
    @httpretty.activate
    def test_no_results(self):
        uri = self.uri_root + '/workout/?started_after=2014-06-01T00%3A00%3A00%2B00%3A00&user=9118466'
        content_returned = '{"_links":{"self":[{"href":"\/v7.0\/workout\/?started_after=2014-06-01T00%3A00%3A00%2B00%3A00&limit=40&user=9118466&offset=0"}],"documentation":[{"href":"https:\/\/www.mapmyapi.com\/docs\/Workout"}]},"_embedded":{"workouts":[]},"total_count":0}'
        httpretty.register_uri(httpretty.GET, uri, body=content_returned, status=200)

        workouts_paginator = self.mmf.workout.search(user=9118466, started_after=datetime.datetime(2014, 6, 1))
        the_page = workouts_paginator.page(1)
        self.assertEqual(str(the_page), '<Page 1 of 1>')
        self.assertEqual(len(the_page), 0)
        self.assertFalse(the_page.has_next())
        self.assertFalse(the_page.has_previous())
        self.assertFalse(the_page.has_other_pages())
        self.assertEqual(the_page.start_index(), 0)
        self.assertEqual(the_page.end_index(), 0)

        self.assertRaisesRegexp(PageNotAnInteger, 'That page number is not an integer',
                                workouts_paginator.page, 'lobster')
        self.assertRaisesRegexp(EmptyPage, 'That page number is less than 1',
                                workouts_paginator.page, -1)
        self.assertRaisesRegexp(EmptyPage, 'That page contains no results',
                                workouts_paginator.page, 2)

    @httpretty.activate
    def test_multiple_pages(self):
        uri_page1 = self.uri_root + '/workout/?started_after=2014-04-01T00%3A00%3A00%2B00%3A00&user=9118466&limit=2'
        uri_page2 = self.uri_root + '/workout/?started_after=2014-04-01T00%3A00%3A00%2B00%3A00&user=9118466&offset=2&limit=2'

        content_returned_page1 = '{"_links":{"self":[{"href":"\/v7.0\/workout\/?started_after=2014-04-01T00%3A00%3A00%2B00%3A00&limit=2&user=9118466&offset=0"}],"documentation":[{"href":"https:\/\/www.mapmyapi.com\/docs\/Workout"}],"next":[{"href":"\/v7.0\/workout\/?started_after=2014-04-01T00%3A00%3A00%2B00%3A00&limit=2&user=9118466&offset=2"}]},"_embedded":{"workouts":[{"start_datetime":"2014-04-02T16:56:52+00:00","name":"Stand Up Paddling on April 2, 2014","updated_datetime":"2014-04-02T18:10:54+00:00","created_datetime":"2014-04-02T18:10:53+00:00","aggregates":{"active_time_total":3857.0,"distance_total":5102.7470208,"cadence_max":66.0,"speed_max":1.7170001728,"speed_min":0.3000000502,"cadence_min":15.0,"speed_avg":1.3230014688,"cadence_avg":63.72,"elapsed_time_total":3856.0,"metabolic_energy_total":1426744.0},"reference_key":"765392205","start_locale_timezone":"America\/Denver","source":"Unknown Garmin Device(006-B1632-00)","_links":{"route":[{"href":"\/v7.0\/route\/383905322\/","id":"383905322"}],"self":[{"href":"\/v7.0\/workout\/524193296\/","id":"524193296"}],"activity_type":[{"href":"\/v7.0\/activity_type\/863\/","id":"863"}],"user":[{"href":"\/v7.0\/user\/9118466\/","id":"9118466"}],"privacy":[{"href":"\/v7.0\/privacy_option\/3\/","id":"3"}]},"has_time_series":true},{"start_datetime":"2014-04-02T22:57:00+00:00","name":"Biked 5.89 mi on Trail-a-bike","updated_datetime":"2014-04-03T03:59:06+00:00","created_datetime":"2014-04-02T23:45:02+00:00","aggregates":{"active_time_total":2123.0,"distance_total":9479.03616,"steps_total":0.0,"speed_avg":4.4659296,"elapsed_time_total":2100.0,"metabolic_energy_total":1029264.0},"reference_key":null,"start_locale_timezone":"America\/Denver","source":"MapMyRun Android App","_links":{"route":[{"href":"\/v7.0\/route\/384185044\/","id":"384185044"}],"self":[{"href":"\/v7.0\/workout\/524561622\/","id":"524561622"}],"activity_type":[{"href":"\/v7.0\/activity_type\/41\/","id":"41"}],"user":[{"href":"\/v7.0\/user\/9118466\/","id":"9118466"}],"privacy":[{"href":"\/v7.0\/privacy_option\/3\/","id":"3"}]},"has_time_series":true}]},"total_count":3}'
        content_returned_page2 = '{"_links":{"prev":[{"href":"\/v7.0\/workout\/?started_after=2014-04-01T00%3A00%3A00%2B00%3A00&limit=2&user=9118466&offset=0"}],"self":[{"href":"\/v7.0\/workout\/?started_after=2014-04-01T00%3A00%3A00%2B00%3A00&limit=2&user=9118466&offset=2"}],"documentation":[{"href":"https:\/\/www.mapmyapi.com\/docs\/Workout"}],"next":[{"href":"\/v7.0\/workout\/?started_after=2014-04-01T00%3A00%3A00%2B00%3A00&limit=2&user=9118466&offset=4"}]},"_embedded":{"workouts":[{"start_datetime":"2014-04-03T23:25:42+00:00","name":"Biked 3.12 mi on 4\/3\/2014","updated_datetime":"2014-04-04T00:02:19+00:00","created_datetime":"2014-04-04T00:02:19+00:00","aggregates":{"active_time_total":2178.0,"distance_total":5018.46567552,"steps_total":0.0,"speed_avg":2.3041603904,"elapsed_time_total":2179.0,"metabolic_energy_total":1054368.0},"reference_key":null,"start_locale_timezone":"America\/Denver","source":"MapMyRun Android App","_links":{"route":[{"href":"\/v7.0\/route\/384844360\/","id":"384844360"}],"self":[{"href":"\/v7.0\/workout\/525585196\/","id":"525585196"}],"activity_type":[{"href":"\/v7.0\/activity_type\/41\/","id":"41"}],"user":[{"href":"\/v7.0\/user\/9118466\/","id":"9118466"}],"privacy":[{"href":"\/v7.0\/privacy_option\/3\/","id":"3"}]},"has_time_series":true}]},"total_count":3}'

        httpretty.register_uri(httpretty.GET, uri_page1, body=content_returned_page1, status=200)
        httpretty.register_uri(httpretty.GET, uri_page2, body=content_returned_page2, status=200)

        workouts_paginator = self.mmf.workout.search(user=9118466, started_after=datetime.datetime(2014, 4, 1), per_page=2)

        self.assertEqual(workouts_paginator.page_range, [1, 2])

        page1 = workouts_paginator.page(1)
        page2 = workouts_paginator.page(2)

        self.assertEqual(page1.next_page_number(), 2)
        self.assertEqual(page2.previous_page_number(), 1)

        self.assertEqual(page1.start_index(), 1)
        self.assertEqual(page1.end_index(), 2)

        self.assertEqual(page2.start_index(), 3)
        self.assertEqual(page2.end_index(), 3)

        self.assertIsInstance(page1[0], WorkoutObject)
