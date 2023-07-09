"""
Test cases for IP Address function.
"""
from django.test import TestCase, RequestFactory
from user_service.views import get_client_ip


class BaseTest(TestCase):
    """
    Base test class for all tests
    """

    def setUp(self):
        self.factory = RequestFactory()
        return super().setUp()


class GetClientIpTest(BaseTest):
    """
    Class to test obtaining an IP Address of a user.
    """

    def test_ip(self):
        """
        Tests if IP can be obtained during the requests.
        """
        request = self.factory.get("/")
        request.META = {
            "HTTP_X_FORWARDED_FOR": "192.168.1.1, 10.0.0.1",
            "REMOTE_ADDR": "127.0.0.1",
        }
        client_ip = get_client_ip(request)
        self.assertEqual(client_ip, "192.168.1.1")
