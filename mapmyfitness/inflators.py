import copy


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
