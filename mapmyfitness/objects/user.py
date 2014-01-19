import datetime

from .base import BaseObject


class UserObject(BaseObject):
    simple_properties = {
        'first_name': None, 'last_name': None, 'username': None,
        'weight': None, 'height': None, 'display_measurement_system': None,
        'time_zone': None, 'email': None, 'gender': None, 'location': None,
    }

    datetime_properties = {
        'last_login': None, 'last_login': 'last_login_datetime',
        'date_joined': 'join_datetime',
    }

    @property
    def id(self):
        return int(self.original_dict['_links']['self'][0]['id'])


    @property
    def birthdate(self):
        return datetime.date.strptime(self.original_dict['birthdate'], '%Y-%m-%d')
