from .base import BaseAPI

from mapmyfitness.inflators import RouteInflator
from mapmyfitness.validators import RouteValidator
from mapmyfitness.serializers import RouteSerializer


class Route(BaseAPI):
    path = '/route'
    validator_class = RouteValidator
    inflator_class = RouteInflator
    serializer_class = RouteSerializer
    embedded_name = 'routes'
