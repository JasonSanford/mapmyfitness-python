import datetime

from .base import BaseValidator


class WorkoutValidator(BaseValidator):
    def validate_create(self):
        # TODO: Ugh, too late to deal with cirular imports
        from ..api.workout import aggregate_values, time_series_values
        obj = self.create_obj

        if 'activity_type' not in obj or ('activity_type' in obj and not isinstance(obj['activity_type'], int)):
            self.add_error('Workout activity_type must exist and be of type int.')

        if 'start_datetime' not in obj or ('start_datetime' in obj and not isinstance(obj['start_datetime'], datetime.datetime)):
            self.add_error('Workout start_datetime must exist and be of type datetime.datetime.')

        for aggregate_value in aggregate_values:
            if aggregate_value in obj and not isinstance(obj[aggregate_value], (int, float)):
                self.add_error('Workout {0} must be of type int or float.'.format(aggregate_value))

        if 'time_series' in obj:
            time_series = obj['time_series']

            # TODO: conditionally use items() Py3, or iteritmes() Py2 here
            for time_series_key, time_series_list in time_series.items():
                if time_series_key in time_series_values:
                    if time_series_key == 'position':
                        positions = time_series['position']
                        for position in positions:
                            is_list = isinstance(position, list)
                            if not is_list or (is_list and len(position) != 2):
                                self.add_error('Workout time_series position must be a 2-list with the first item being of type int or float and the second item being a dict.')
                            else:
                                position_dict = position[1]
                                for lat_or_lng in ('lat', 'lng'):
                                    if lat_or_lng not in position_dict:
                                        self.add_error('Workout time_series position dict must have a {0} key and be of type int or float.'.format(lat_or_lng))
                    else:
                        for item in time_series[time_series_key]:
                            is_list = isinstance(item, list)
                            if not is_list or (is_list and len(item) != 2) or (is_list and len(item) == 2 and (not isinstance(item[0], (int, float)) or not isinstance(item[1], (int, float)))):
                                self.add_error('Workout time_series {0} must be a 2-list with each item being of type int or float.'.format(time_series_key))

    def validate_search(self):
        search_kwargs = self.search_kwargs

        if 'user' not in search_kwargs or ('user' in search_kwargs and not isinstance(search_kwargs['user'], int)):
            self.add_error('Workout user must exist and be of type int.')

        datetime_args = ['updated_before', 'updated_after', 'created_before', 'created_after', 'started_before', 'started_after']
        for datetime_arg in datetime_args:
            if datetime_arg in search_kwargs and not isinstance(search_kwargs[datetime_arg], datetime.datetime):
                self.add_error('Workout {0} must be of type datetime.datetime.'.format(datetime_arg))

        if 'activity_type' in search_kwargs and not isinstance(search_kwargs['activity_type'], int):
            self.add_error('Workout activity_type must be of type int.')
