from django.http import HttpRequest
from django.test import TestCase

from wagtail.wagtailcore.models import Site

from flags.models import FlagState
from flags.state import (
    flag_state,
    flag_enabled,
    flag_disabled
)


class FlagStateTestCase(TestCase):
    def setUp(self):
        self.site = Site.objects.get(is_default_site=True)
        self.request = HttpRequest()
        self.request.site = self.site

    def test_non_existent_flag(self):
        """ Non-existent flags always have a default state of False """
        self.assertFalse(flag_state('FLAG_DOES_NOT_EXIST'))

    def test_flag_state_enabled(self):
        """ Global flags that are enabled should be True """
        self.assertTrue(flag_state('FLAG_ENABLED'))

    def test_flag_state_disabled(self):
        """ Global flags that are disabled should be False """
        self.assertFalse(flag_state('FLAG_DISABLED'))

    def test_flag_state_bool_false_and_db_site_true(self):
        """ Test state of multiple conditions, one 'site' in database """
        FlagState.objects.create(name='FLAG_DISABLED',
                                 condition='site',
                                 value=str(self.site))
        self.assertTrue(flag_state('FLAG_DISABLED', request=self.request))

    def test_flag_state_bool_true_and_db_site_true(self):
        """ Test state of multiple conditions, one 'site' in database """
        FlagState.objects.create(name='FLAG_ENABLED',
                                 condition='site',
                                 value=str(self.site))
        self.assertTrue(flag_state('FLAG_ENABLED', request=self.request))

    def test_flag_state_non_existent_flag_site(self):
        """ Given a site non-existent flags should still be False """
        self.assertFalse(flag_state('FLAG_DOES_NOT_EXIST',
                                    request=self.request))

    def test_flag_state_site_for_other_site(self):
        """ A site flag enabled for another site should be False """
        other_site = Site.objects.create(
            is_default_site=False,
            root_page_id=self.site.root_page_id,
            hostname='other.host'
        )
        FlagState.objects.create(name='DB_FLAG',
                                 condition='site',
                                 value=str(other_site))
        self.assertFalse(flag_state('DB_FLAG', request=self.request))

    def test_flag_state_site_for_multiple_sites(self):
        """ A site flag enabled for two sites should return True for both """
        other_site = Site.objects.create(
            is_default_site=False,
            root_page_id=self.site.root_page_id,
            hostname='other.host'
        )
        FlagState.objects.create(name='DB_FLAG',
                                 condition='site',
                                 value=str(other_site))
        FlagState.objects.create(name='DB_FLAG',
                                 condition='site',
                                 value=str(self.site))
        self.assertTrue(flag_state('DB_FLAG', request=self.request))

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
