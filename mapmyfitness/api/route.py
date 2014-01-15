from .base import BaseAPI
from ..inflators import RouteInflator
from ..validators import RouteValidator
from ..serializers import RouteSerializer


class Route(BaseAPI):
    path = '/route'
    validator_class = RouteValidator
    inflator_class = RouteInflator
    serializer_class = RouteSerializer
    embedded_name = 'routes'
