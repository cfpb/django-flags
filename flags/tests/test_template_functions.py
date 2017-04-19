from django.http import HttpRequest
from django.test import TestCase

from wagtail.wagtailcore.models import Site

from flags.template_functions import flag_disabled, flag_enabled


class TemplateFunctionsTestCase(TestCase):
    def setUp(self):
        self.site = Site.objects.get(is_default_site=True)
        self.request = HttpRequest()
        self.request.site = self.site

    def test_flag_enabled_true(self):
        self.assertTrue(flag_enabled('FLAG_ENABLED', request=self.request))

    def test_flag_enabled_false(self):
        self.assertFalse(flag_enabled('FLAG_DISABLED', request=self.request))

    def test_flag_disabled_true(self):
        self.assertTrue(flag_disabled('FLAG_DISABLED', request=self.request))

    def test_flag_disabled_false(self):
        self.assertFalse(flag_disabled('FLAG_ENABLED', request=self.request))
