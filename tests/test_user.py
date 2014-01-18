import copy

import httpretty

from mapmyfitness.exceptions import BadRequestException, InvalidObjectException, InvalidSearchArgumentsException
from mapmyfitness.objects.user import UserObject
from mapmyfitness.serializers import UserSerializer

from tests import MapMyFitnessTestCase
#from tests.valid_objects import user as valid_user


class UserTest(MapMyFitnessTestCase):
    def test_cannot_delete(self):
        try:
            self.mmf.user.delete(1234)
        except Exception as exc:
            self.assertIsInstance(exc, AttributeError)
            self.assertEqual(str(exc), "'User' object has no attribute 'delete'")


    def test_cannot_create(self):
        try:
            self.mmf.user.create(1234)
        except Exception as exc:
            self.assertIsInstance(exc, AttributeError)
            self.assertEqual(str(exc), "'User' object has no attribute 'create'")


    def test_cannot_update(self):
        try:
            self.mmf.user.update(1234)
        except Exception as exc:
            self.assertIsInstance(exc, AttributeError)
            self.assertEqual(str(exc), "'User' object has no attribute 'update'")
