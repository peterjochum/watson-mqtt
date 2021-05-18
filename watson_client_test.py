import unittest

from watson_client import WatsonMQTTDevice


class TestWatsonClient(unittest.TestCase):
    test_device = "foodev"
    test_organization = "testorg"
    test_device_type = "testtype"
    test_auth_type = "use-token-auth"
    test_token = "12345"

    def setUp(self):
        self.c = WatsonMQTTDevice(
            self.test_device,
            self.test_organization,
            self.test_device_type,
            self.test_auth_type,
            self.test_token,
        )

    def test_get_client_id(self):
        device_str = self.c.get_client_id()
        self.assertEqual("d:testorg:testtype:foodev", device_str)

    def test_get_connect_url(self):
        connect_url = self.c.get_connect_url()
        expected = "testorg.messaging.internetofthings.ibmcloud.com"
        self.assertEqual(expected, connect_url)

    def test_auth_setter(self):
        self.c.auth_type = self.test_auth_type
        self.assertEqual(self.test_auth_type, self.c.auth_type)

    def test_auth_setter_unsupported(self):
        try:
            # This should trigger an attribute error
            self.c.auth_type = "unsupported-super-auth"
            self.fail("No AttributeError was triggered by unsupported auth")
        except AttributeError:
            pass


if __name__ == "__main__":
    unittest.main()
