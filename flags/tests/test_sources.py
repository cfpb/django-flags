from unittest.mock import Mock

from django.http import HttpRequest
from django.test import TestCase, override_settings

from flags.models import FlagState
from flags.sources import (
    Condition,
    DatabaseFlagsSource,
    Flag,
    SettingsFlagsSource,
    get_flags,
)


# Test flag source for using this module to test
class TestFlagsSource:
    def get_flags(self):
        return {
            "SOURCED_FLAG": [Condition("boolean", True)],
            "NOT_IN_SETTINGS_FLAG": [Condition("boolean", False)],
        }


class ExceptionalFlagsSource:
    def get_flags(self):
        raise Exception("This flag source is exceptional!")


class SettingsFlagsSourceTestCase(TestCase):
    @override_settings(FLAGS={"MY_FLAG": [("boolean", True)]})
    def test_get_flags_two_tuple(self):
        source = SettingsFlagsSource()
        flags = source.get_flags()
        self.assertEqual(
            flags,
            {"MY_FLAG": [Condition("boolean", True, required=False)]},
        )

    @override_settings(FLAGS={"MY_FLAG": [("boolean", True, True)]})
    def test_get_flags_three_tuple(self):
        source = SettingsFlagsSource()
        flags = source.get_flags()
        self.assertEqual(
            flags, {"MY_FLAG": [Condition("boolean", True, required=True)]}
        )

    @override_settings(
        FLAGS={
            "MY_FLAG": [
                {"condition": "boolean", "value": True, "required": True},
            ]
        }
    )
    def test_get_flags_list_of_dicts(self):
        source = SettingsFlagsSource()
        flags = source.get_flags()
        self.assertEqual(
            flags, {"MY_FLAG": [Condition("boolean", True, required=True)]}
        )

    @override_settings(
        FLAGS={"MY_FLAG": [{"condition": "boolean", "value": True}]}
    )
    def test_get_flags_list_of_dicts_without_required(self):
        source = SettingsFlagsSource()
        flags = source.get_flags()
        self.assertEqual(
            flags,
            {"MY_FLAG": [Condition("boolean", True, required=False)]},
        )


class DatabaseFlagsSourceTestCase(TestCase):
    def test_get_flags(self):
        FlagState.objects.create(
            name="MY_FLAG", condition="boolean", value="False"
        )
        source = DatabaseFlagsSource()
        flags = source.get_flags()
        self.assertEqual(flags, {"MY_FLAG": [Condition("boolean", "False")]})


class ConditionTestCase(TestCase):
    def test_check_fn_none(self):
        condition = Condition("nonexistent", "value")
        result = condition.check()
        self.assertIsNone(result)


class FlagTestCase(TestCase):
    def test_eq(self):
        flag1 = Flag("MY_FLAG")
        flag2 = Flag("MY_FLAG")
        self.assertEqual(flag1, flag2)

    def test_conditions(self):
        flag = Flag("MY_FLAG", [Condition("boolean", True)])
        self.assertEqual(len(list(flag.conditions)), 1)

    def test_check_state(self):
        flag = Flag("MY_FLAG", [Condition("boolean", True)])
        self.assertTrue(flag.check_state())

    def test_check_state_no_conditions(self):
        flag = Flag("MY_FLAG", [])
        self.assertFalse(flag.check_state())

    def test_check_state_multiple_conditions_not_required(self):
        request = Mock(path="/foo")
        flag = Flag(
            "MY_FLAG",
            [Condition("boolean", False), Condition("path matches", "/foo")],
        )
        self.assertTrue(flag.check_state(request=request))

    def test_check_state_multiple_conditions_required(self):
        request = Mock(path="/foo")
        flag = Flag(
            "MY_FLAG",
            [
                Condition("boolean", True, required=True),
                Condition("path matches", "/foo", required=True),
            ],
        )
        self.assertTrue(flag.check_state(request=request))

    def test_check_state_multiple_conditions_required_failure(self):
        request = Mock(path="/foo")
        flag = Flag(
            "MY_FLAG",
            [
                Condition("boolean", False, required=True),
                Condition("path matches", "/foo", required=True),
            ],
        )
        self.assertFalse(flag.check_state(request=request))

    @override_settings(FLAGS_STATE_LOGGING=True)
    def test_flag_check_state_logs_state(self):
        flag = Flag(
            "MY_FLAG",
            [Condition("boolean", False), Condition("path matches", "/foo")],
        )
        with self.assertLogs("flags.sources", level="INFO") as logger:
            flag.check_state(request=Mock(path="/bar"))
            flag.check_state(request=Mock(path="/foo"))

        self.assertEqual(
            logger.output,
            [
                "INFO:flags.sources:Flag MY_FLAG evaluated False with "
                "conditions: boolean (False), path matches (False).",
                "INFO:flags.sources:Flag MY_FLAG evaluated True with "
                "conditions: boolean (False), path matches (True).",
            ],
        )


class GetFlagsTestCase(TestCase):
    def test_get_flags_from_sources(self):
        flags = get_flags(sources=["flags.tests.test_sources.TestFlagsSource"])
        self.assertTrue(flags["SOURCED_FLAG"].conditions[0].value)
        self.assertIn("NOT_IN_SETTINGS_FLAG", flags)

    def test_add_flags_from_sources_non_existent(self):
        with self.assertRaises(ImportError):
            get_flags(sources=["non.existent.module"])

    @override_settings(FLAGS={"SOURCED_FLAG": [], "OTHER_FLAG": []})
    def test_get_flags(self):
        flags = get_flags(
            sources=[
                "flags.sources.SettingsFlagsSource",
                "flags.tests.test_sources.TestFlagsSource",
            ]
        )
        self.assertIn("OTHER_FLAG", flags)
        self.assertIn("SOURCED_FLAG", flags)
        self.assertEqual(len(flags["OTHER_FLAG"].conditions), 0)
        self.assertEqual(len(flags["SOURCED_FLAG"].conditions), 1)

    @override_settings(FLAGS={"MY_FLAG": []})
    def test_get_flags_ensure_combined_conditions_work(self):
        FlagState.objects.create(
            name="MY_FLAG", condition="boolean", value="True"
        )
        flags = get_flags(
            sources=[
                "flags.sources.SettingsFlagsSource",
                "flags.sources.DatabaseFlagsSource",
            ]
        )
        self.assertIn("MY_FLAG", flags)
        my_flag = flags["MY_FLAG"]
        self.assertTrue(my_flag.check_state())

    def test_ignore_errors(self):
        # Without ignore_errors
        with self.assertRaises(Exception):  # noqa: B017
            get_flags(
                sources=["flags.tests.test_sources.ExceptionalFlagsSource"]
            )

        # With ignore_errors
        flags = get_flags(
            sources=["flags.tests.test_sources.ExceptionalFlagsSource"],
            ignore_errors=True,
        )
        self.assertEqual(flags, {})

    def test_caches_flags_on_request_if_provided(self):
        request = HttpRequest()
        self.assertFalse(hasattr(request, "flag_conditions"))
        get_flags(request=request)
        self.assertIsInstance(request.flag_conditions, dict)

    def test_uses_cached_flags_from_request(self):
        request = HttpRequest()

        # The initial call looks up flag conditions from the database source.
        with self.assertNumQueries(1):
            get_flags(request=request)

        # Subsequent calls with a request object don't need to redo the lookup
        # because they have the cached flags.
        with self.assertNumQueries(0):
            get_flags(request=request)

        # But subsequent calls without a request object still redo the lookup.
        with self.assertNumQueries(1):
            get_flags()
