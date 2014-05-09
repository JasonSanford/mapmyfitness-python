import datetime

import httpretty

from mapmyfitness.exceptions import PageNotAnInteger, EmptyPage
from mapmyfitness.objects.user import UserObject
from mapmyfitness.serializers import UserSerializer
from mapmyfitness.utils import iso_format_to_datetime

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