from django.apps import apps
from django.test import TestCase

from shorturls.apps import UrlShortenerConfig


class test_appConfig(TestCase):

    """Check if the app is registered and the correct app is returned"""

    def test_app(self):
        self.assertEqual("shorturls", UrlShortenerConfig.name)
        self.assertEqual("shorturls", apps.get_app_config("shorturls").name)
