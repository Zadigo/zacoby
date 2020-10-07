import unittest
from zacoby.driver.remote import RemoteConnection

class TestRemoteConnection(unittest.TestCase):
    def setUp(self):
        self.remote_server_address = 'https://localhost:8000'
        self.remote = RemoteConnection
        self.remote.remote_server_address = self.remote_server_address

    def test_remote_instance(self):
        self.assertNotIsInstance(self.remote.as_class(
            self.remote_server_address), type
        )
        self.assertIsNotNone(self.remote.remote_server_address)

    def test_build_url(self):
        url = 'https://localhost:8000/session'
        self.assertEqual(
            self.remote._build_url(self.remote, ['POST', '/session']), url
        )

    def test_can_send_request(self):
        response = self.remote._request(
            self.remote, 'POST', 'https://example.com'
        )
        self.assertIsInstance(response, dict)


if __name__ == "__main__":
    unittest.main()
