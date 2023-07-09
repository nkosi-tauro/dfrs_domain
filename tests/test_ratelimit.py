"""
Test cases for user_service
"""
from django.core.cache import caches
from datetime import timedelta
from django.test import TestCase, RequestFactory
from user_service.views import get_client_ip
from user_service.ratelimit import RateLimitExceeded, RateLimit


class BaseTest(TestCase):
    """
    Base test class for all tests
    """

    def setUp(self):
        # Test Admin user
        self.factory = RequestFactory()
        request = self.factory.get("/")
        ip_address = get_client_ip(request)
        self.cache = caches["default"]

        self.rate_limit = RateLimit(
            key=ip_address,
            limit=5,
            period=10,
            cache=self.cache,
            key_prefix="rl:",
        )

        return super().setUp()

class RateLimitTest(BaseTest):
    """
    Class to test rate limits of the logins.
    """

    def test_rate_limit_above_limit(self):
        """
        Method to test if the Exception has been successfully raised after too many login attempts.
        """
        with self.assertRaises(RateLimitExceeded) as cm:
            self.rate_limit.check(6)
        self.assertEqual(cm.exception.limit, self.rate_limit.limit)

    def test_custom_period_as_timedelta(self):
        """
        Checks timedelta period option
        """
        custom_rate_limit = RateLimit(
            key="",
            limit=10,
            period=timedelta(minutes=30),
            cache=self.cache,
            key_prefix="rl:",
        )
        self.assertEqual(custom_rate_limit.seconds, 1800)

    def test_custom_period_as_seconds(self):
        """
        Checks seconds period option
        """
        custom_rate_limit = RateLimit(
            key="",
            limit=10,
            period=3600,
            cache=self.cache,
            key_prefix="rl:",
        )
        self.assertEqual(custom_rate_limit.seconds, 3600)
