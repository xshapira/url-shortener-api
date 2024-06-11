from django.test import TestCase
from django.urls import resolve, reverse

from shorturls.views import ShortUrlView, redirect_to_url


class TestUrl(TestCase):
    """
    Tests for creating new short URLs and redirecting to the full URLs they point to. Includes also a test for handling non-existent short URLs.
    """

    def test_create_url_resolves(self):
        url = reverse("create")
        self.assertEqual(resolve(url).func.view_class, ShortUrlView)

    def test_redirect_url_resolves(self):
        url = reverse("entry_point", args=["some-url"])
        self.assertEqual(resolve(url).func, redirect_to_url)

    def test_redirect_url_404(self):
        url = reverse("entry_point", args=["some-url"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
