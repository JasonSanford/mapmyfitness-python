from .base import BaseAPI
from ..serializers import ActivityTypeSerializer
from .mixins import Findable


class ActivityType(BaseAPI, Findable):
    path = '/activity_type'
    serializer_class = ActivityTypeSerializer
    embedded_name = 'activity_types'
