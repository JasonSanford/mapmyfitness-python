import datetime
import inspect

from .base import BaseObject
from ..exceptions import AttributeNotFoundException, InvalidSizeException


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
        # First checking to see if we're entering a recursion
        # cycle, and if so exiting immediately. Calling `hasattr(self, name)`
        # will call getattr(self, name) itself and therefore keep recursing.
        if '__getattr__' in inspect.stack()[1]:
            raise AttributeNotFoundException

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
            dt = datetime.datetime.strptime(self.original_dict['birthdate'], '%Y-%m-%d')
            return dt.date()

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

    def get_profile_photo(self, size='medium'):
        if size not in ('small', 'medium', 'large'):
            raise InvalidSizeException('User get_profile_photo size must one of "small", "medium" or "large".')
        from mapmyfitness import MapMyFitness
        instance = MapMyFitness.instance()
        user_profile_photo = instance._user_profile_photo.find(self.id)
        return getattr(user_profile_photo, size)


class UserProfilePhotoObject(BaseObject):
    @property
    def small(self):
        return self.original_dict['_links']['small'][0]['href']

    @property
    def medium(self):
        return self.original_dict['_links']['medium'][0]['href']

    @property
    def large(self):
        return self.original_dict['_links']['large'][0]['href']
