from .base import BaseAPI
from mapmyfitness.inflators import WorkoutInflator
from mapmyfitness.validators import WorkoutValidator
from mapmyfitness.serializers import WorkoutSerializer


class Workout(BaseAPI):
    path = '/workout'
    validator_class = WorkoutValidator
    inflator_class = WorkoutInflator
    serializer_class = WorkoutSerializer
    embedded_name = 'workouts'
