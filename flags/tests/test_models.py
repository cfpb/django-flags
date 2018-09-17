from django.core.cache import cache
from django.test import TestCase, override_settings

from flags.models import FlagState


class FlagStateTestCase(TestCase):

    def test_flag_str(self):
        state = FlagState.objects.create(
            name='MY_FLAG',
            condition='boolean',
            value='True'
        )
        self.assertEqual(
            str(state),
            'MY_FLAG is enabled when boolean is True'
        )

    @override_settings(FLAGS_CACHE_CONDITIONS=True)
    def test_save_signal_receiver(self):
        cache.set('flags', ('test conditions', 'value', None))
        self.assertIsNotNone(cache.get('flags'))
        FlagState.objects.create(
            name='MY_FLAG',
            condition='boolean',
            value='True'
        )
        self.assertIsNone(cache.get('flags_conditions_MY_FLAG'))

    @override_settings(FLAGS_CACHE_CONDITIONS=True)
    def test_delete_signal_receiver(self):
        state = FlagState.objects.create(
            name='MY_FLAG',
            condition='boolean',
            value='True'
        )
        cache.set('flags', ('test conditions', 'value', None))
        self.assertIsNotNone(cache.get('flags'))
        state.delete()
        self.assertIsNone(cache.get('flags'))
