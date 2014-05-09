from .api.config import APIConfig
from .api.route import Route
from .api.activity_type import ActivityType
from .api.user import User, UserProfilePhoto
from .api.workout import Workout
from .exceptions import NotInitializedException


class MapMyFitness(object):
    """
    Creating a singleton instance of this class, so that we can easily referr to
    it from anywhere in the code without re-creating the instance and again
    providing the api_key and access_token.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MapMyFitness, cls).__new__(cls)

        return cls._instance

    def __init__(self, api_key, access_token, cache_finds=False):
        api_config = APIConfig(api_key=api_key, access_token=access_token)
        self.route = Route(api_config=api_config, cache_finds=cache_finds)
        self.workout = Workout(api_config=api_config, cache_finds=cache_finds)
        self.user = User(api_config=api_config, cache_finds=cache_finds)
        self._user_profile_photo = UserProfilePhoto(api_config=api_config, cache_finds=cache_finds)
        self.activity_type = ActivityType(api_config=api_config, cache_finds=cache_finds)

    @classmethod
    def instance(cls):
        """
        Returns the singleton instance of MapMyFitness if initializaed.
        If there is no initialized singleton instance, it raises a not initialized exception.

        ::raises:: NotInitializedException
        """
        if cls._instance:
            return cls._instance

        raise NotInitializedException("MapMyFitness has not been initialized")

    @classmethod
    def _drop(cls):
        """
        Drops the instance of the singleton (for testing purposes)
        """
        cls._instance = None
