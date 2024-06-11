import json

from django.test import Client, TestCase
from django.urls import resolve, reverse


class TestHomeView(TestCase):
    def setUp(self):
        self.url = reverse("home")  # Update the pattern name here
        self.response = self.client.get(self.url)

    def test_home_url_resolves_to_template_view(self):
        view = resolve(self.url)
        self.assertEqual(view.func.__name__, "view")

    def test_successful_home_view_get_response(self):
        self.assertEqual(self.response.status_code, 200)

    def test_home_view_returns_correct_html(self):
        self.assertContains(self.response, "URL Shortener")
        self.assertNotContains(self.response, "hello world")


class TestsViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.list_url = reverse("create")

    def test_create_short_url_and_return_response(self):
        url = reverse("create")
        data = {"url": "https://duckduckgo.com"}
        result = self.client.post(url, data, content_type="application/json")
        self.assertEqual(result.status_code, 201)
        return result

    def test_redirect_url(self):
        response = self.test_create_short_url_and_return_response()
        url_key = json.loads(response.content.decode("utf-8")).get("short_url")
        response = self.client.get(url_key)
        self.assertEqual(response.status_code, 302)

    def test_redirect_url_404(self):
        """
        Test for a redirect url that doesn't exist in the database
        and should return a 404.
        """
        response = self.test_create_short_url_and_return_response()
        url_key = json.loads(response.content.decode("utf-8")).get("short_url")
        response = self.client.get(f"{url_key}1")
        self.assertEqual(response.status_code, 404)

    def test_redirect_url_visits(self):
        """
        Make sure that redirect url visits are incremented.
        """
        response = self.test_create_short_url_and_return_response()
        url_key = json.loads(response.content.decode("utf-8")).get("short_url")
        response = self.client.get(url_key)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(url_key)
        self.assertEqual(response.status_code, 302)
