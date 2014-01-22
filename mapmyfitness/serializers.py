from .objects.route import RouteObject
from .objects.workout import WorkoutObject
from .objects.user import UserObject


class BaseSerializer(object):
    def __init__(self, dict_):
        obj = self.object_class(dict_)
        self.serialized = obj


class RouteSerializer(BaseSerializer):
    object_class = RouteObject


class WorkoutSerializer(BaseSerializer):
    object_class = WorkoutObject


class UserSerializer(BaseSerializer):
    object_class = UserObject
