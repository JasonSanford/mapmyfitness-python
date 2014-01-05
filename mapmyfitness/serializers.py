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

        self.serialized = serialized