from django.apps import apps
from django.core.checks import Warning
from django.test import TestCase, override_settings

from flags.checks import flag_conditions_check


class TestFlagsConditionsCheck(TestCase):
    @override_settings(FLAGS={"FLAG_TO_CHECK": [("boolean", True)]})
    def test_check_passes_if_conditions_exist_with_valid_value(self):
        self.assertFalse(flag_conditions_check(apps.get_app_configs()))

    @override_settings(FLAGS={"FLAG_TO_CHECK": [("nonexistent", "value")]})
    def test_check_fails_if_conditions_do_not_exist(self):
        errors = flag_conditions_check(apps.get_app_configs())
        self.assertEqual(len(errors), 1)
        self.assertIsInstance(errors[0], Warning)
        self.assertEqual(errors[0].id, "flags.E001")

    @override_settings(FLAGS={"FLAG_TO_CHECK": [("boolean", "foo")]})
    def test_check_fails_if_conditions_exist_with_invalid_value(self):
        errors = flag_conditions_check(apps.get_app_configs())
        self.assertEqual(len(errors), 1)
        self.assertIsInstance(errors[0], Warning)
        self.assertEqual(errors[0].id, "flags.E002")
