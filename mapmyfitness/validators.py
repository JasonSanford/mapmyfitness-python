from .exceptions import ValidatorException


class BaseValidator(object):
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

    def validate_find(self):
        pass

    def validate_search(self):
        """This should be overridden by subclasses of BaseValidator"""

    def __repr__(self):
        if len(self.errors):
            return ' '.join(self.errors)


class RouteValidator(BaseValidator):
    def validate_create(self):
        pass

    def validate_find(self):
        pass

    def validate_search(self):
        if 'user' not in self.search_kwargs and 'users' not in self.search_kwargs and 'close_to_location' not in self.search_kwargs:
            self.add_error('Either a user, users or close_to_location argument must be passed to search for routes.')
            return