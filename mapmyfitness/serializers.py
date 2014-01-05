import copy


class BaseSerializer(object):
    def __init__(self, obj):
        self.initial_obj = obj
        self.serialize()


class RouteSerializer(BaseSerializer):
    def serialize(self):
        serialized = copy.deepcopy(self.initial_obj)

        serialized['starting_location'] = {
            'type': 'Point',
            'coordinates': [
                serialized['points'][0]['lng'],
                serialized['points'][0]['lat']
            ]
        }

        serialized.setdefault('_links', {})

        serialized['_links']['privacy'] = [{
                'href': '/v7.0/privacy_option/{0}/'.format(serialized['privacy']),
                'id': '{0}'.format(serialized['privacy'])
            }]

        self.serialized = serialized