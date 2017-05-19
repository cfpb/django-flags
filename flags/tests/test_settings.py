try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock

from django.test import TestCase, override_settings

import flags.settings

from flags.models import FlagState

from flags.settings import (
    DuplicateFlagException,
    Flag,
    add_flags_from_sources,
    get_flags
)

# Test flag for using this module to test
SOURCED_FLAG = True


class FlagTestCase(TestCase):

    def test_eq(self):
        flag1 = Flag('MY_FLAG')
        flag2 = Flag('MY_FLAG')
        self.assertEqual(flag1, flag2)

    def test_configured_conditions(self):
        flag = Flag('MY_FLAG', {'boolean': True})
        # Check the conditions length
        self.assertEqual(len(list(flag.configured_conditions)), 1)

    def test_dynamic_conditions(self):
        # Add a dyanmic (database) condition
        flag = Flag('MY_FLAG')
        FlagState.objects.create(name='MY_FLAG',
                                 condition='parameter',
                                 value='MY_FLAG')
        self.assertEqual(len(list(flag.dynamic_conditions)), 1)

    def test_conditions(self):
        flag = Flag('MY_FLAG', {'boolean': True})
        FlagState.objects.create(name='MY_FLAG',
                                 condition='parameter',
                                 value='MY_FLAG')
        self.assertEqual(len(list(flag.conditions)), 2)

    def test_check_state(self):
        flag = Flag('MY_FLAG', {'boolean': True})
        self.assertTrue(flag.check_state())

    def test_check_state_no_conditions(self):
        flag = Flag('MY_FLAG', {})
        self.assertFalse(flag.check_state())

    def test_check_state_multiple_conditions(self):
        request = Mock(path='/foo')
        flag = Flag('MY_FLAG', {'boolean': False, 'path': '/foo'})
        self.assertTrue(flag.check_state(request=request))


class SettingsTestCase(TestCase):

    def tearDown(self):
        # Reset SOURCED_FLAGS after each test
        flags.settings.SOURCED_FLAGS = {}

    def test_add_flags_from_sources(self):
        add_flags_from_sources(sources=['flags.tests.test_settings'])
        self.assertTrue(flags.settings.SOURCED_FLAGS['SOURCED_FLAG'])

    def test_add_flags_from_sources_non_existent(self):
        with self.assertRaises(ImportError):
            add_flags_from_sources(sources=['non.existent.module'])

    @override_settings(FLAGS={'GLOBAL_FLAG': {}})
    def test_get_flags(self):
        add_flags_from_sources(sources=['flags.tests.test_settings'])
        self.assertIn('GLOBAL_FLAG', get_flags())
        self.assertIn('SOURCED_FLAG', get_flags())

    @override_settings(FLAGS={'SOURCED_FLAG': {}})
    def test_duplicate_global_flags(self):
        with self.assertRaises(DuplicateFlagException):
            add_flags_from_sources(sources=['flags.tests.test_settings'])
