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