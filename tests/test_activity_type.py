import httpretty

from mapmyfitness.serializers import ActivityTypeSerializer

from tests import MapMyFitnessTestCase


class UserTest(MapMyFitnessTestCase):
    def test_cannot_delete(self):
        try:
            self.mmf.activity_type.delete(1234)
        except Exception as exc:
            self.assertIsInstance(exc, AttributeError)
            self.assertEqual(str(exc), "'ActivityType' object has no attribute 'delete'")

    def test_cannot_create(self):
        try:
            self.mmf.activity_type.create(1234)
        except Exception as exc:
            self.assertIsInstance(exc, AttributeError)
            self.assertEqual(str(exc), "'ActivityType' object has no attribute 'create'")

    def test_cannot_update(self):
        try:
            self.mmf.activity_type.update(1234)
        except Exception as exc:
            self.assertIsInstance(exc, AttributeError)
            self.assertEqual(str(exc), "'ActivityType' object has no attribute 'update'")

    @httpretty.activate
    def test_find(self):
        uri_child = self.uri_root + '/activity_type/38'
        uri_root = self.uri_root + '/activity_type/11'

        content_returned_child = '{"mets":8.0,"mets_speed":[{"mets":"4","speed":4.4704},{"mets":"6","speed":4.91744},{"mets":"8","speed":5.81152},{"mets":"10","speed":6.7056},{"mets":"12","speed":7.8232},{"mets":"16","speed":8.9408}],"name":"Touring Bike","short_name":null,"has_children":true,"_links":{"icon_url":[{"href":"http:\/\/static.mapmyfitness.com\/d\/website\/activity_icons\/bike.png"}],"self":[{"href":"\/v7.0\/activity_type\/38\/","id":"38"}],"documentation":[{"href":"https:\/\/www.mapmyapi.com\/docs\/Activity_Type"}],"root":[{"href":"\/v7.0\/activity_type\/11\/","id":"11"}],"parent":[{"href":"\/v7.0\/activity_type\/11\/","id":"11"}]}}'
        content_returned_root = '{"mets":8.0,"mets_speed":[{"mets":"4","speed":4.4704},{"mets":"6","speed":4.91744},{"mets":"8","speed":5.81152},{"mets":"10","speed":6.7056},{"mets":"12","speed":7.8232},{"mets":"16","speed":8.9408}],"name":"Bike Ride","short_name":"bike","has_children":true,"_links":{"icon_url":[{"href":"http:\/\/static.mapmyfitness.com\/d\/website\/activity_icons\/bike.png"}],"self":[{"href":"\/v7.0\/activity_type\/11\/","id":"11"}],"documentation":[{"href":"https:\/\/www.mapmyapi.com\/docs\/Activity_Type"}],"root":[{"href":"\/v7.0\/activity_type\/11\/","id":"11"}],"parent":[{"href":"\/v7.0\/activity_type\/11\/","id":"11"}]}}'

        httpretty.register_uri(httpretty.GET, uri_child, body=content_returned_child, status=200)
        httpretty.register_uri(httpretty.GET, uri_root, body=content_returned_root, status=200)

        activity_type_child = self.mmf.activity_type.find(38)
        self.assertEqual(activity_type_child.id, 38)
        self.assertTrue(activity_type_child.has_parent)
        self.assertEqual(activity_type_child.root_activity_type_id, 11)
        self.assertEqual(activity_type_child.root_activity_type.name, 'Bike Ride')
        self.assertEqual(activity_type_child.root_activity_type.name, 'Bike Ride')  # Calling again retrieves the cached value

        activity_type_root = self.mmf.activity_type.find(11)
        self.assertEqual(activity_type_root.root_activity_type.id, 11)

    def test_serializer(self):
        activity_type_json = {"mets":8.0,"mets_speed":[{"mets":"4","speed":4.4704},{"mets":"6","speed":4.91744},{"mets":"8","speed":5.81152},{"mets":"10","speed":6.7056},{"mets":"12","speed":7.8232},{"mets":"16","speed":8.9408}],"name":"Touring Bike","short_name":None,"has_children":True,"_links":{"icon_url":[{"href":"http:\/\/static.mapmyfitness.com\/d\/website\/activity_icons\/bike.png"}],"self":[{"href":"\/v7.0\/activity_type\/38\/","id":"38"}],"documentation":[{"href":"https:\/\/www.mapmyapi.com\/docs\/Activity_Type"}],"root":[{"href":"\/v7.0\/activity_type\/11\/","id":"11"}],"parent":[{"href":"\/v7.0\/activity_type\/11\/","id":"11"}]}}
        serializer = ActivityTypeSerializer(activity_type_json)
        activity_type = serializer.serialized

        self.assertEqual(activity_type.id, 38)
        self.assertEqual(activity_type.name, 'Touring Bike')
