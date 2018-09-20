from django.test import TestCase, override_settings

from flags.models import FlagState
from flags.sources import DatabaseFlagsSource, SettingsFlagsSource


class SettingsFlagsSourceTestCase(TestCase):

    @override_settings(FLAGS={'MY_FLAG': {'boolean': True}})
    def test_get_flags(self):
        source = SettingsFlagsSource()
        flags = source.get_flags()
        self.assertEqual(flags, {'MY_FLAG': {'boolean': True}})


class DatabaseFlagsSourceTestCase(TestCase):

    def test_get_flags(self):
        FlagState.objects.create(
            name='MY_FLAG',
            condition='boolean',
            value='True'
        )
        source = DatabaseFlagsSource()
        flags = source.get_flags()
        self.assertEqual(flags, {'MY_FLAG': {'boolean': 'True'}})
