try:
    from unittest.mock import Mock
except ImportError:  # pragma: no cover
    from mock import Mock

from django.test import TestCase, override_settings

from flags.settings import Flag, get_flags, get_flags_from_sources


# Test flag source for using this module to test
class TestFlagsSource(object):
    def get_flags(self):
        return {
            'SOURCED_FLAG': {'boolean': True},
            'NOT_IN_SETTINGS_FLAG': {'boolean': False}
        }


class FlagTestCase(TestCase):

    def test_eq(self):
        flag1 = Flag('MY_FLAG')
        flag2 = Flag('MY_FLAG')
        self.assertEqual(flag1, flag2)

    def test_conditions(self):
        flag = Flag('MY_FLAG', {'boolean': True})
        self.assertEqual(len(list(flag.conditions)), 1)

    def test_check_state(self):
        flag = Flag('MY_FLAG', {'boolean': True})
        self.assertTrue(flag.check_state())

    def test_check_state_no_conditions(self):
        flag = Flag('MY_FLAG', {})
        self.assertFalse(flag.check_state())

    def test_check_state_multiple_conditions(self):
        request = Mock(path='/foo')
        flag = Flag('MY_FLAG', {'boolean': False, 'path matches': '/foo'})
        self.assertTrue(flag.check_state(request=request))


class SettingsTestCase(TestCase):

    def test_get_flags_from_sources(self):
        sourced_flags = get_flags_from_sources(
            sources=['flags.tests.test_settings.TestFlagsSource', ]
        )
        self.assertTrue(sourced_flags['SOURCED_FLAG']['boolean'])
        self.assertIn('NOT_IN_SETTINGS_FLAG', sourced_flags)

    def test_add_flags_from_sources_non_existent(self):
        with self.assertRaises(ImportError):
            get_flags_from_sources(sources=['non.existent.module'])

    @override_settings(FLAGS={'SOURCED_FLAG': {}, 'OTHER_FLAG': {}})
    def test_get_flags(self):
        sourced_flags = get_flags_from_sources(
            sources=[
                'flags.sources.SettingsFlagsSource',
                'flags.tests.test_settings.TestFlagsSource',
            ]
        )
        flags = get_flags(sourced_flags=sourced_flags)
        self.assertIn('OTHER_FLAG', flags)
        self.assertIn('SOURCED_FLAG', flags)
        self.assertEqual(len(flags['OTHER_FLAG'].conditions), 0)
        self.assertEqual(len(flags['SOURCED_FLAG'].conditions), 1)
