from .exceptions import ValidatorException


class BaseValidator(object):
    def __init__(self, creating_obj=None, searching_kwargs=None):
        if creating_obj is None and searching_kwargs is None:
            raise ValidatorException('Either creating_obj or searching_kwargs must be passed when instantiating a validator.')
        if creating_obj is not None:
            self.creating_obj = creating_obj
        else:  # searching_kwargs is not None
            self.searching_kwargs = searching_kwargs
        self.errors = []
        
        if hasattr(self, 'creating_obj'):
            self.validate_create()
        else:  # hasattr(self, 'searching_kwargs')
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
    def validate_create(self):
        pass

    def validate_search(self):
        if 'user' not in self.searching_kwargs and 'users' not in self.searching_kwargs and 'close_to_location' not in self.searching_kwargs:
            self.add_error('Either a user, users or close_to_location argument must be passed to search for routes.')
            return