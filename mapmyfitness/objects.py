class BaseObject(object):
    def __init__(self, dict_):
        self.original_dict = dict_


class RouteObject(BaseObject):
    @property
    def name(self):
        return self.original_dict['name']

    @property
    def description(self):
        return self.original_dict['description']

    @property
    def distance(self):
        return self.original_dict['distance']

    def points(self, geojson=False):
        _points = self.original_dict['points']

        if geojson:
            return {'type': 'LineString', 'coordinates': [(p['lng'], p['lat']) for p in _points]}

        return _points