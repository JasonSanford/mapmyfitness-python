import copy

from .utils import datetime_to_iso_format

class BaseInflator(object):
    def __init__(self, obj):
        self.initial_obj = obj
        self.inflate()


class RouteInflator(BaseInflator):
    def inflate(self):
        inflated = copy.deepcopy(self.initial_obj)

        inflated['starting_location'] = {
            'type': 'Point',
            'coordinates': [
                inflated['points'][0]['lng'],
                inflated['points'][0]['lat']
            ]
        }

        inflated.setdefault('_links', {})

        inflated['_links']['privacy'] = [{
            'href': '/v7.0/privacy_option/{0}/'.format(inflated['privacy']),
            'id': '{0}'.format(inflated['privacy'])
        }]

        self.inflated = inflated


class WorkoutInflator(BaseInflator):
    def inflate(self):
        # TODO: Ugh, too late to deal with cirular imports
        from .api.workout import aggregate_values
        inflated = copy.deepcopy(self.initial_obj)

        inflated['start_datetime'] = datetime_to_iso_format(inflated['start_datetime'])
        inflated['start_locale_timezone'] = 'UTC'

        inflated['activity_type'] = '/v7.0/activity_type/{0}/'.format(inflated['activity_type'])

        inflated['aggregates'] = {}
        for aggregate_value in aggregate_values:
            if aggregate_value in inflated:
                inflated['aggregates'][aggregate_value] = inflated[aggregate_value]

        self.inflated = inflated
