import six

import warnings
from unittest import skipIf

from django.test import TestCase, override_settings

from flags.conditions import (
    RequiredForCondition,
    register as register_condition,
)
from flags.models import FlagState
from flags.sources import (
    Condition,
    DatabaseFlagsSource,
    Flag,
    SettingsFlagsSource,
    get_flags,
)


try:
    from unittest.mock import Mock
except ImportError:  # pragma: no cover
    from mock import Mock


@register_condition('condition_with_required_arg')
def condition_with_kwarg(condition, required_arg=None, **kwargs):
    if required_arg is None:
        raise RequiredForCondition('required_arg required')


# Test flag source for using this module to test
class TestFlagsSource(object):
    def get_flags(self):
        return {
            'SOURCED_FLAG': [Condition('boolean', True), ],
            'NOT_IN_SETTINGS_FLAG': [
                Condition('boolean', False),
            ],
        }


class ExceptionalFlagsSource(object):
    def get_flags(self):
        raise Exception('This flag source is exceptional!')


class SettingsFlagsSourceTestCase(TestCase):

    @override_settings(FLAGS={'MY_FLAG': {'boolean': True}})
    def test_get_flags_dict(self):
        source = SettingsFlagsSource()
        with warnings.catch_warnings(record=True) as warning_list:
            flags = source.get_flags()
            self.assertTrue(
                any(item.category == FutureWarning for item in warning_list)
            )

        self.assertEqual(
            flags,
            {'MY_FLAG': [Condition('boolean', True, required=False), ]}
        )

    @override_settings(FLAGS={'MY_FLAG': [('boolean', True), ]})
    def test_get_flags_two_tuple(self):
        source = SettingsFlagsSource()
        flags = source.get_flags()
        self.assertEqual(
            flags,
            {'MY_FLAG': [Condition('boolean', True, required=False), ]}
        )

    @override_settings(FLAGS={'MY_FLAG': [('boolean', True, True), ]})
    def test_get_flags_three_tuple(self):
        source = SettingsFlagsSource()
        flags = source.get_flags()
        self.assertEqual(
            flags,
            {'MY_FLAG': [Condition('boolean', True, required=True), ]}
        )

    @override_settings(FLAGS={'MY_FLAG': [
        {
            'condition': 'boolean',
            'value': True,
            'required': True
        },
    ]})
    def test_get_flags_list_of_dicts(self):
        source = SettingsFlagsSource()
        flags = source.get_flags()
        self.assertEqual(
            flags,
            {'MY_FLAG': [Condition('boolean', True, required=True), ]}
        )

    @override_settings(FLAGS={'MY_FLAG': [
        {
            'condition': 'boolean',
            'value': True,
        },
    ]})
    def test_get_flags_list_of_dicts_without_required(self):
        source = SettingsFlagsSource()
        flags = source.get_flags()
        self.assertEqual(
            flags,
            {'MY_FLAG': [Condition('boolean', True, required=False), ]}
        )


class DatabaseFlagsSourceTestCase(TestCase):

    def test_get_flags(self):
        FlagState.objects.create(
            name='MY_FLAG',
            condition='boolean',
            value='False'
        )
        source = DatabaseFlagsSource()
        flags = source.get_flags()
        self.assertEqual(flags, {'MY_FLAG': [Condition('boolean', 'False'), ]})


class ConditionTestCase(TestCase):

    def test_check_fn_none(self):
        condition = Condition('nonexistent', 'value')
        result = condition.check()
        self.assertIsNone(result)

    def test_check_fn_true(self):
        condition = Condition('boolean', True)
        result = condition.check()
        self.assertTrue(result)

    def test_check_evaluates_false_without_required_arg(self):
        condition = Condition('condition_with_required_arg', True)
        result = condition.check()
        self.assertFalse(result)

    @skipIf(six.PY2, 'assertLogs is not available in Python 2.7')
    def test_check_logs_missing_required_arg(self):
        condition = Condition('condition_with_required_arg', True)
        with self.assertLogs('flags.sources', level='INFO') as logger:
            condition.check()

        self.assertIn(
            'Missing required argument for condition',
            logger.output[0]
        )


class FlagTestCase(TestCase):

    def test_eq(self):
        flag1 = Flag('MY_FLAG')
        flag2 = Flag('MY_FLAG')
        self.assertEqual(flag1, flag2)

    def test_conditions(self):
        flag = Flag('MY_FLAG', [Condition('boolean', True)])
        self.assertEqual(len(list(flag.conditions)), 1)

    def test_check_state(self):
        flag = Flag('MY_FLAG', [Condition('boolean', True)])
        self.assertTrue(flag.check_state())

    def test_check_state_no_conditions(self):
        flag = Flag('MY_FLAG', [])
        self.assertFalse(flag.check_state())

    def test_check_state_multiple_conditions_not_required(self):
        request = Mock(path='/foo')
        flag = Flag('MY_FLAG', [
            Condition('boolean', False),
            Condition('path matches', '/foo')
        ])
        self.assertTrue(flag.check_state(request=request))

    def test_check_state_multiple_conditions_required(self):
        request = Mock(path='/foo')
        flag = Flag('MY_FLAG', [
            Condition('boolean', True, required=True),
            Condition('path matches', '/foo', required=True)
        ])
        self.assertTrue(flag.check_state(request=request))

    def test_check_state_multiple_conditions_required_failure(self):
        request = Mock(path='/foo')
        flag = Flag('MY_FLAG', [
            Condition('boolean', False, required=True),
            Condition('path matches', '/foo', required=True)
        ])
        self.assertFalse(flag.check_state(request=request))


class GetFlagsTestCase(TestCase):

    def test_get_flags_from_sources(self):
        flags = get_flags(
            sources=['flags.tests.test_sources.TestFlagsSource', ]
        )
        self.assertTrue(flags['SOURCED_FLAG'].conditions[0].value)
        self.assertIn('NOT_IN_SETTINGS_FLAG', flags)

    def test_add_flags_from_sources_non_existent(self):
        with self.assertRaises(ImportError):
            get_flags(sources=['non.existent.module'])

    @override_settings(FLAGS={'SOURCED_FLAG': [], 'OTHER_FLAG': []})
    def test_get_flags(self):
        flags = get_flags(
            sources=[
                'flags.sources.SettingsFlagsSource',
                'flags.tests.test_sources.TestFlagsSource',
            ]
        )
        self.assertIn('OTHER_FLAG', flags)
        self.assertIn('SOURCED_FLAG', flags)
        self.assertEqual(len(flags['OTHER_FLAG'].conditions), 0)
        self.assertEqual(len(flags['SOURCED_FLAG'].conditions), 1)

    def test_ignore_errors(self):
        # Without ignore_errors
        with self.assertRaises(Exception):
            get_flags(
                sources=['flags.tests.test_sources.ExceptionalFlagsSource', ]
            )

        # With ignore_errors
        flags = get_flags(
            sources=['flags.tests.test_sources.ExceptionalFlagsSource', ],
            ignore_errors=True
        )
        self.assertEqual(flags, {})
