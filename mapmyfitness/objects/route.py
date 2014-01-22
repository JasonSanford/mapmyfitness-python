from .base import BaseObject
from ..utils import privacy_enum_to_string


class RouteObject(BaseObject):
    simple_properties = {
        'name': None, 'description': None, 'distance': None,
        'total_ascent': 'ascent', 'total_descent': 'descent',
        'min_elevation': None, 'max_elevation': None,
        'city': None, 'state': None, 'country': None,
    }

    datetime_properties = {
        'created_datetime': None, 'updated_datetime': None,
    }

    @property
    def id(self):
        return int(self.original_dict['_links']['self'][0]['id'])

    @property
    def privacy(self):
        privacy_enum = int(self.original_dict['_links']['privacy'][0]['id'])
        return privacy_enum_to_string(privacy_enum)

    def points(self, geojson=False):
        _points = self.original_dict['points']

        if geojson:
            return {'type': 'LineString', 'coordinates': [(p['lng'], p['lat']) for p in _points]}

        return _points
