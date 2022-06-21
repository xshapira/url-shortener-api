from django.test import TestCase
from django.urls import resolve, reverse

from shorturls.views import ShortUrlView, redirect_to_url


class TestUrl(TestCase):

    """Tests for creating and redirecting a short URL.
    And a test for non-existing short URL"""

    def test_create_url_resolves(self):
        url = reverse("create")
        self.assertEqual(resolve(url).func.view_class, ShortUrlView)

    def test_redirect_url_resolves(self):
        url = reverse("redirect", args=["some-url"])
        self.assertEqual(resolve(url).func, redirect_to_url)

    def test_redirect_url_404(self):
        url = reverse("redirect", args=["some-url"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
