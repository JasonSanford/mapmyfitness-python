import datetime

from .base import BaseObject
from ..utils import iso_format_to_datetime


class UserObject(BaseObject):
    @property
    def id(self):
        return int(self.original_dict['_links']['self'][0]['id'])

    @property
    def first_name(self):
        return self.original_dict['first_name']

    @property
    def last_name(self):
        return self.original_dict['last_name']

    @property
    def username(self):
        return self.original_dict['username']

    @property
    def weight(self):
        return self.original_dict['weight']

    @property
    def height(self):
        return self.original_dict['height']

    @property
    def display_measurement_system(self):
        return self.original_dict['display_measurement_system']

    @property
    def time_zone(self):
        return self.original_dict['time_zone']

    @property
    def birthdate(self):
        return datetime.datetime.strptime(self.original_dict['birthdate'], '%Y-%m-%d')

    @property
    def last_login(self):
        return iso_format_to_datetime(self.original_dict['last_login'])