from .base import BaseObject
from ..utils import privacy_enum_to_string


class WorkoutObject(BaseObject):
    simple_properties = {
        'name': None, 'start_locale_timezone': None, 'source': None,
        'has_time_series': None,
    }

    datetime_properties = {
        'start_datetime': None, 'created_datetime': None, 'updated_datetime': None,
    }

    @property
    def id(self):
        return int(self.original_dict['_links']['self'][0]['id'])

    @property
    def time_series(self):
        if self.has_time_series:
            if 'time_series' in self.original_dict:
                return self.original_dict['time_series']
            elif hasattr(self, '_time_series'):
                return self._time_series
            else:
                from mapmyfitness import MapMyFitness
                instance = MapMyFitness.instance()
                workout = instance.workout.find(self.id)
                self._time_series = workout.time_series
                return self._time_series

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

    @property
    def route(self):
        if self.route_id:
            if hasattr(self, '_route'):
                return self._route
            else:
                from mapmyfitness import MapMyFitness
                instance = MapMyFitness.instance()
                route = instance.route.find(self.route_id)
                self._route = route
                return self._route

    @property
    def route_id(self):
        links = self.original_dict['_links']
        if 'route' in links:
            return int(links['route'][0]['id'])

    @property
    def activity_type_id(self):
        return int(self.original_dict['_links']['activity_type'][0]['id'])

    @property
    def activity_type(self):
        if hasattr(self, '_activity_type'):
            return self._activity_type
        else:
            from mapmyfitness import MapMyFitness
            instance = MapMyFitness.instance()
            activity_type = instance.activity_type.find(self.activity_type_id)
            self._activity_type = activity_type
            return self._activity_type

    @property
    def privacy(self):
        privacy_enum = int(self.original_dict['_links']['privacy'][0]['id'])
        return privacy_enum_to_string(privacy_enum)
