from .api import APIConfig, Route


class MapMyFitness(object):
    def __init__(self, key, version='7.0'):
        api_config = APIConfig(key=key, version=version)
        self.route = Route(api_config=api_config)
