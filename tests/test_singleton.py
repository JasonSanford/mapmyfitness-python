from tests import MapMyFitnessTestCase
from mapmyfitness import MapMyFitness
from mapmyfitness.exceptions import NotInitializedException


class MapMyFitnessSingleton(MapMyFitnessTestCase):
    def tearDown(self):
        MapMyFitness._drop()

    def test_MapMyFitness_is_singleton(self):
        mmf1 = MapMyFitness('api-key1', 'access_token1')
        mmf2 = MapMyFitness('api-key2', 'access_token2')
        
        assert mmf1 == mmf2


    def test_MapMyFitness_singleton_not_initialized(self):
        MapMyFitness._drop()
        try:
            MapMyFitness.instance()
        except NotInitializedException:
            pass
        else:
            assert False  # We should have raised the exception

