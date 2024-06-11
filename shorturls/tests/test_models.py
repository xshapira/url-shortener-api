from django.test import TestCase

from shorturls.models import ShortUrl


class ShortUrlModelTest(TestCase):
    @classmethod
    # This method is called before each test is run
    def setUpTestData(cls):
        cls.url_ = ShortUrl.objects.create(
            long_url="https://duckduckgo.com", key="slight", visits=1
        )

    def test_long_url_field(self):
        self.assertEqual(self.url_.long_url, str(self.url_.long_url))

    def test_model_returns_key_string(self):
        self.assertEqual(self.url_.key, str(self.url_.key))

    def test_model_returns_visits_int(self):
        self.assertEqual(self.url_.visits, int(self.url_.visits))

    def test_save_method(self):
        methods = self.url_
        self.assertEqual(methods.save, self.url_.save)

    def test_update_method(self):
        methods = self.url_
        self.assertEqual(methods.update, self.url_.update)

    def test_generate_key_method(self):
        methods = self.url_
        self.assertEqual(methods.generate_key, self.url_.generate_key)
