from mapmyfitness.constants import PUBLIC, PRIVATE, FRIENDS

from .exceptions import ValidatorException


class BaseValidator(object):
    privacy_options = (PUBLIC, PRIVATE, FRIENDS)

    def type_or_types_to_str(self, type_or_types):
        def repr_to_str(repr):
            return repr.split(" '")[1].split("'>")[0]
        if isinstance(type_or_types, (list, tuple)):
            types = []
            for repr in type_or_types:
                types.append(repr_to_str(str(repr)))
            return ' or '.join(types)
        else:
            return repr_to_str(str(type_or_types))

    def __init__(self, create_obj=None, search_kwargs=None):
        if create_obj is None and search_kwargs is None:
            raise ValidatorException('Either create_obj or search_kwargs must be passed when instantiating a validator.')
        if create_obj is not None:
            self.create_obj = create_obj
        else:  # search_kwargs is not None
            self.search_kwargs = search_kwargs
        self.errors = []
        
        if hasattr(self, 'create_obj'):
            self.validate_create()
        else:  # hasattr(self, 'search_kwargs')
            self.validate_search()

    def add_error(self, error):
        if error not in self.errors:
            self.errors.append(error)

    @property
    def valid(self):
        return len(self.errors) == 0

    def validate_create(self):
        """This should be overridden by subclasses of BaseValidator"""

    def validate_search(self):
        """This should be overridden by subclasses of BaseValidator"""

    def __repr__(self):
        if len(self.errors):
            return ' '.join(self.errors)


class RouteValidator(BaseValidator):
    required_members = {
        'name': str,
        'city': str,
        'country': str,
        'distance': (int, float),
        'points': (list, tuple),
    }

    def validate_create(self):
        obj = self.create_obj

        for required_member, type_or_types in self.required_members.items():
            if required_member not in obj or (required_member in obj and not isinstance(obj[required_member], type_or_types)):
                    self.add_error('Route {0} must exist and be of type {1}.'.format(required_member, self.type_or_types_to_str(type_or_types)))

        if 'privacy' not in obj or ('privacy' in obj and obj['privacy'] not in self.privacy_options):
            self.add_error('Route privacy must exist and be one of constants.PUBLIC, constants.PRIVATE or constants.FRIENDS.')

        for point in obj['points']:
            if not isinstance(point, dict):
                self.add_error('Each point in Route points must be of type dict.')
                break
            for required in ('lat', 'lng'):
                if required not in point or (required in point and not isinstance(point[required], (int, float))):
                    self.add_error('Each point in Route points must have a "{0}" key and be of type int or float.'.format(required))

    def validate_search(self):
        def _bad_close_to_location():
            self.add_error('Route close_to_location must be a list or 2-tuple of latitude,longitude.')
        def _bad_users():
            self.add_error('Route users must be a list or tuple of ints.')

        if 'user' not in self.search_kwargs and 'users' not in self.search_kwargs and 'close_to_location' not in self.search_kwargs:
            self.add_error('Either a user, users or close_to_location argument must be passed to search for routes.')
            return
        if 'user' in self.search_kwargs:
            try:
                int(self.search_kwargs['user'])
            except ValueError:
                self.add_error('Route user must be of type int.')
        elif 'users' in self.search_kwargs:
            if not isinstance(self.search_kwargs['users'], (list, tuple)):
                _bad_users()
                return
            users = self.search_kwargs['users']
            for user in users:
                try:
                    int(user)
                except ValueError:
                    _bad_users()
        else:  # close_to_location
            lat_lng = self.search_kwargs['close_to_location']
            if len(lat_lng) != 2:
                _bad_close_to_location()
            else:
                for coord in lat_lng:
                    try:
                        float(coord)
                    except ValueError:
                        _bad_close_to_location()
                        break