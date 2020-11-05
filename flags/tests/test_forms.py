from django.test import TestCase

from flags.conditions.registry import _conditions, register
from flags.forms import FlagStateForm


class FormTestCase(TestCase):
    def test_valid_data(self):
        """
        Validate the state.

        Args:
            self: (todo): write your description
        """
        form = FlagStateForm(
            {"name": "FLAG_ENABLED", "condition": "boolean", "value": "True"}
        )
        self.assertTrue(form.is_valid())
        state = form.save()
        self.assertEqual(state.name, "FLAG_ENABLED")
        self.assertEqual(state.condition, "boolean")
        self.assertEqual(state.value, "True")

    def test_blank_data(self):
        """
        Validate that the form.

        Args:
            self: (todo): write your description
        """
        form = FlagStateForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors,
            {
                "name": ["This field is required."],
                "condition": ["This field is required."],
                "value": ["This field is required."],
            },
        )

    def test_bad_data(self):
        """
        Validate bad bad bad bad bad bad bad data.

        Args:
            self: (todo): write your description
        """
        form = FlagStateForm(
            {"name": "FLAG_ENABLED", "condition": "boolean", "value": "flase"}
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors,
            {"value": ["Enter one of 'on', 'off', 'true', 'false', etc."]},
        )

    def test_condition_choices_are_bound_late(self):
        """
        Dynamically create custom fields to use.

        Args:
            self: (todo): write your description
        """
        @register("fake_condition")
        def fake_condition():
            """
            Returns true if the given condition.

            Args:
            """
            return True  # pragma: no cover

        def cleanup_condition(condition_name):
            """
            Cleanup a condition from the condition name.

            Args:
                condition_name: (str): write your description
            """
            del _conditions[condition_name]

        self.addCleanup(cleanup_condition, "fake_condition")

        form = FlagStateForm()
        self.assertIn(
            ("fake_condition", "fake_condition"),
            form.fields["condition"].choices,
        )
