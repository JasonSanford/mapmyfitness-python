from .base import BaseObject
from ..utils import privacy_enum_to_string, iso_format_to_datetime


class RouteObject(BaseObject):
    @property
    def id(self):
        return int(self.original_dict['_links']['self'][0]['id'])

    @property
    def name(self):
        return self.original_dict['name']

    @property
    def description(self):
        return self.original_dict['description']

    @property
    def distance(self):
        return self.original_dict['distance']

    @property
    def ascent(self):
        return self.original_dict['total_ascent']

    @property
    def descent(self):
        return self.original_dict['total_descent']

    @property
    def min_elevation(self):
        return self.original_dict['min_elevation']

    @property
    def max_elevation(self):
        return self.original_dict['max_elevation']

    @property
    def city(self):
        return self.original_dict['city']

    @property
    def state(self):
        return self.original_dict['state']

    @property
    def country(self):
        return self.original_dict['country']

    @property
    def privacy(self):
        privacy_enum = int(self.original_dict['_links']['privacy'][0]['id'])
        return privacy_enum_to_string(privacy_enum)

    @property
    def created_datetime(self):
        return iso_format_to_datetime(self.original_dict['created_datetime'])

    @property
    def updated_datetime(self):
        return iso_format_to_datetime(self.original_dict['updated_datetime'])

    def points(self, geojson=False):
        _points = self.original_dict['points']

        if geojson:
            return {'type': 'LineString', 'coordinates': [(p['lng'], p['lat']) for p in _points]}

        return _points
