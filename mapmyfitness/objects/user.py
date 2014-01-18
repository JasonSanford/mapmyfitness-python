from mapmyfitness.utils import privacy_enum_to_string, iso_format_to_datetime
from .base import BaseObject


class UserObject(BaseObject):
    @property
    def id(self):
        return int(self.original_dict['_links']['self'][0]['id'])
