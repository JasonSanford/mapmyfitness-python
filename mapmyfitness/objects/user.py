import datetime

from .base import BaseObject


class UserObject(BaseObject):
    simple_properties = {
        'first_name': None, 'last_name': None, 'username': None,
        'time_zone': None, 'gender': None, 'location': None,
    }

    datetime_properties = {
        'last_login': None, 'last_login': 'last_login_datetime',
        'date_joined': 'join_datetime',
    }

    def __getattr__(self, name):
        from mapmyfitness import MapMyFitness
        instance = MapMyFitness.instance()
        user = instance.user.find(self.id)
        self.__init__(user.original_dict)
        return getattr(self, name)

    @property
    def id(self):
        return int(self.original_dict['_links']['self'][0]['id'])

    @property
    def birthdate(self):
        if 'birthdate' in self.original_dict:
            return datetime.date.strptime(self.original_dict['birthdate'], '%Y-%m-%d')

    @property
    def email(self):
        if 'email' in self.original_dict:
            return self.original_dict['email']

    @property
    def display_measurement_system(self):
        if 'display_measurement_system' in self.original_dict:
            return self.original_dict['display_measurement_system']

    @property
    def weight(self):
        if 'weight' in self.original_dict:
            return self.original_dict['weight']

    @property
    def height(self):
        if 'height' in self.original_dict:
            return self.original_dict['height']
