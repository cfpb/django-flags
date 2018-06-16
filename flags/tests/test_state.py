from django.http import HttpRequest
from django.test import TestCase

from flags.state import flag_disabled, flag_enabled, flag_state


class FlagStateTestCase(TestCase):
    def setUp(self):
        self.request = HttpRequest()

    def test_non_existent_flag(self):
        """ Non-existent flags always have a default state of False """
        self.assertFalse(flag_state('FLAG_DOES_NOT_EXIST'))

    def test_flag_state_enabled(self):
        """ Global flags that are enabled should be True """
        self.assertTrue(flag_state('FLAG_ENABLED'))

    def test_flag_state_disabled(self):
        """ Global flags that are disabled should be False """
        self.assertFalse(flag_state('FLAG_DISABLED'))

    def test_flag_state_non_existent_flag_site(self):
        """ Given a site non-existent flags should still be False """
        self.assertFalse(flag_state('FLAG_DOES_NOT_EXIST',
                                    request=self.request))

    def test_flag_enabled_enabled(self):
        """ Global flags enabled should be True """
        self.assertTrue(flag_enabled('FLAG_ENABLED'))

    def test_flag_enabled_disabled(self):
        """ Global flags disabled should be False """
        self.assertFalse(flag_enabled('FLAG_DISABLED'))

    def test_flag_disabled_global_disabled(self):
        """ Global flags disabled should be True """
        self.assertTrue(flag_disabled('FLAG_DISABLED'))

    def test_flag_disabled_global_enabled(self):
        """ Global flags enabled should be False """
        self.assertFalse(flag_disabled('FLAG_ENABLED'))
