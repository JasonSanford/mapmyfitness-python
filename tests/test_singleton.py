from tests import MapMyFitnessTestCase
from mapmyfitness import MapMyFitness

class MapMyFitnessSingleton(MapMyFitnessTestCase):
    def test_MapMyFitness_is_singleton(self):
        mmf1 = MapMyFitness('api-key1', 'access_token1')
        mmf2 = MapMyFitness('api-key2', 'access_token2')
        
        assert mmf1 == mmf2
