from .api import APIConfig, Route


class MapMyFitness(object):
    PRIVATE = 0
    PUBLIC = 3
    FRIENDS = 1

    def __init__(self, api_key, access_token):
        api_config = APIConfig(api_key=api_key, access_token=access_token)
        self.route = Route(api_config=api_config)
