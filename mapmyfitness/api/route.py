from .base import BaseAPI
from ..inflators import RouteInflator
from ..validators.route import RouteValidator
from ..serializers import RouteSerializer
from .mixins import Deleteable, Searchable, Createable, Findable, Updateable


class Route(BaseAPI, Deleteable, Searchable, Createable, Findable, Updateable):
    path = '/route'
    validator_class = RouteValidator
    inflator_class = RouteInflator
    serializer_class = RouteSerializer
    embedded_name = 'routes'
