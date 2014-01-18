from .base import BaseAPI
from ..inflators import UserInflator
from ..validators import UserValidator
from ..serializers import UserSerializer
from .mixins import Searchable, Createable, Findable, Updateable


class User(BaseAPI, Searchable, Findable):
    path = '/user'
    validator_class = UserValidator
    inflator_class = UserInflator
    serializer_class = UserSerializer
    embedded_name = 'users'
