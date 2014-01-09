from .utils import privacy_enum_to_string, iso_format_to_datetime


class BaseObject(object):
    def __init__(self, dict_):
        self.original_dict = dict_


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


class WorkoutObject(BaseObject):
    @property
    def id(self):
        return int(self.original_dict['_links']['self'][0]['id'])

    @property
    def name(self):
        return self.original_dict['name']

    @property
    def start_datetime(self):
        return iso_format_to_datetime(self.original_dict['start_datetime'])

    @property
    def created_datetime(self):
        return iso_format_to_datetime(self.original_dict['created_datetime'])

    @property
    def updated_datetime(self):
        return iso_format_to_datetime(self.original_dict['updated_datetime'])

    @property
    def start_locale_timezone(self):
        return self.original_dict['start_locale_timezone']

    @property
    def source(self):
        return self.original_dict['source']

    #
    # Aggregates
    #

    # These should always exist
    @property
    def active_time_total(self):
        return self.original_dict['aggregates']['active_time_total']

    @property
    def distance_total(self):
        return self.original_dict['aggregates']['distance_total']

    @property
    def steps_total(self):
        return self.original_dict['aggregates']['steps_total']

    @property
    def elapsed_time_total(self):
        return self.original_dict['aggregates']['elapsed_time_total']

    @property
    def metabolic_energy_total(self):
        return self.original_dict['aggregates']['metabolic_energy_total']

    # These might not exist
    @property
    def speed_max(self):
        if 'speed_max' in self.original_dict['aggregates']:
            return self.original_dict['aggregates']['speed_max']

    @property
    def speed_avg(self):
        if 'speed_avg' in self.original_dict['aggregates']:
            return self.original_dict['aggregates']['speed_avg']

    #
    # Links - TODO: return not _id, but the actual object
    #
    @property
    def route_id(self):
        links = self.original_dict['_links']
        if 'route' in links:
            return int(links['route'][0]['id'])

    @property
    def activity_type_id(self):
        return int(self.original_dict['_links']['activity_type'][0]['id'])

    @property
    def privacy(self):
        privacy_enum = int(self.original_dict['_links']['privacy'][0]['id'])
        return privacy_enum_to_string(privacy_enum)
