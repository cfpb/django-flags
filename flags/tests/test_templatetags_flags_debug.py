from django.test import TestCase, override_settings

from flags.sources import get_flags
from flags.templatetags.flags_debug import (
    bool_enabled,
    conditions_without_bool,
    required_conditions_without_bool,
    state_str,
)


class TestWagtailFlagsAdminTemplateTags(TestCase):
    @override_settings(FLAGS={"MYFLAG": [("boolean", True)]})
    def test_enabled_enabled(self):
        """
        Determine if enabled

        Args:
            self: (todo): write your description
        """
        flag = get_flags().get("MYFLAG")
        self.assertTrue(bool_enabled(flag))

    @override_settings(FLAGS={"MYFLAG": [("boolean", False)]})
    def test_enabled_disabled(self):
        """
        Check if enabled

        Args:
            self: (todo): write your description
        """
        flag = get_flags().get("MYFLAG")
        self.assertFalse(bool_enabled(flag))

    @override_settings(
        FLAGS={"MYFLAG": [("boolean", True), ("path matches", "/mypath")]}
    )
    def test_conditions(self):
        """
        Test if the condition is condition.

        Args:
            self: (todo): write your description
        """
        flag = get_flags().get("MYFLAG")
        self.assertEqual(len(conditions_without_bool(flag)), 1)

    @override_settings(
        FLAGS={
            "MYFLAG": [
                ("path matches", "/mypath", True),
                ("path matches", "/myotherpath"),
            ]
        }
    )
    def test_required_conditions(self):
        """
        Asserts the conditions are required.

        Args:
            self: (todo): write your description
        """
        flag = get_flags().get("MYFLAG")
        self.assertEqual(len(required_conditions_without_bool(flag)), 1)


class TestStateStrTemplateTag(TestCase):
    @override_settings(FLAGS={"MYFLAG": [("anonymous", "False", True)]})
    def test_state_str_required_no_non_required_no_bool(self):
        """
        Check if the state of the test.

        Args:
            self: (todo): write your description
        """
        flag = get_flags().get("MYFLAG")
        self.assertEqual(
            "MYFLAG is <b>enabled</b> when <i>all</i> required conditions "
            "are met.",
            state_str(flag),
        )

    @override_settings(
        FLAGS={"MYFLAG": [("anonymous", "False", True), ("boolean", True)]}
    )
    def test_state_str_required_no_non_required_bool_true(self):
        """
        Test if the test case is true or false.

        Args:
            self: (todo): write your description
        """
        flag = get_flags().get("MYFLAG")
        self.assertEqual(
            "MYFLAG is <b>enabled</b> when <i>all</i> required conditions "
            "are met.",
            state_str(flag),
        )

    @override_settings(
        FLAGS={"MYFLAG": [("anonymous", "False", True), ("boolean", False)]}
    )
    def test_state_str_required_no_non_required_bool_false(self):
        """
        Test if the state of the condition.

        Args:
            self: (todo): write your description
        """
        flag = get_flags().get("MYFLAG")
        self.assertEqual(
            "MYFLAG is <b>disabled</b> for all requests, "
            "even when <i>all</i> required conditions are met.",
            state_str(flag),
        )

    @override_settings(
        FLAGS={
            "MYFLAG": [
                ("anonymous", "False", True),
                ("path matches", "/mypath"),
                ("boolean", False),
            ]
        }
    )
    def test_state_str_required_non_required_bool_false(self):
        """
        Test if the state of the test is set.

        Args:
            self: (todo): write your description
        """
        flag = get_flags().get("MYFLAG")
        self.assertEqual(
            "MYFLAG is <b>enabled</b> when <i>all</i> required conditions "
            "and <i>any</i> non-required condition is met.",
            state_str(flag),
        )

    @override_settings(
        FLAGS={
            "MYFLAG": [
                ("anonymous", "False", True),
                ("boolean", True, True),
                ("path matches", "/mypath"),
            ]
        }
    )
    def test_state_str_required_non_required_bool_true_required(self):
        """
        Test if the state of the test is true.

        Args:
            self: (todo): write your description
        """
        flag = get_flags().get("MYFLAG")
        self.assertEqual(
            "MYFLAG is <b>enabled</b> for all requests.", state_str(flag)
        )

    @override_settings(
        FLAGS={
            "MYFLAG": [
                ("anonymous", "False", True),
                ("boolean", False, True),
                ("path matches", "/mypath"),
            ]
        }
    )
    def test_state_str_required_non_required_bool_false_required(self):
        """
        Test if the state of a test.

        Args:
            self: (todo): write your description
        """
        flag = get_flags().get("MYFLAG")
        self.assertEqual(
            "MYFLAG is <b>disabled</b> for all requests.", state_str(flag)
        )

    @override_settings(
        FLAGS={"MYFLAG": [("anonymous", "False"), ("boolean", True)]}
    )
    def test_state_str_no_required_non_required_bool_true(self):
        """
        Test if the state of the condition.

        Args:
            self: (todo): write your description
        """
        flag = get_flags().get("MYFLAG")
        self.assertEqual(
            "MYFLAG is <b>enabled</b> for all requests.", state_str(flag)
        )

    @override_settings(
        FLAGS={
            "MYFLAG": [
                ("anonymous", "False", True),
                ("path matches", "/mypath"),
            ]
        }
    )
    def test_state_str_required_non_required_no_bool(self):
        """
        Test if the state of the test is set.

        Args:
            self: (todo): write your description
        """
        flag = get_flags().get("MYFLAG")
        self.assertEqual(
            "MYFLAG is <b>enabled</b> when <i>all</i> required conditions "
            "and <i>any</i> non-required condition is met.",
            state_str(flag),
        )

    @override_settings(
        FLAGS={
            "MYFLAG": [
                ("anonymous", "False", True),
                ("path matches", "/mypath"),
                ("boolean", True),
            ]
        }
    )
    def test_state_str_required_non_required_bool(self):
        """
        Test if the test.

        Args:
            self: (todo): write your description
        """
        flag = get_flags().get("MYFLAG")
        self.assertEqual(
            "MYFLAG is <b>enabled</b> when <i>all</i> required conditions "
            "are met.",
            state_str(flag),
        )

    @override_settings(FLAGS={"MYFLAG": [("path matches", "/mypath")]})
    def test_state_str_non_bool_non_required(self):
        """
        Test if the state of the test is true.

        Args:
            self: (todo): write your description
        """
        flag = get_flags().get("MYFLAG")
        self.assertEqual(
            "MYFLAG is <b>enabled</b> when <i>any</i> condition " "is met.",
            state_str(flag),
        )

    @override_settings(FLAGS={"MYFLAG": [("boolean", False)]})
    def test_state_str_bool_false(self):
        """
        Test if the test is false.

        Args:
            self: (todo): write your description
        """
        flag = get_flags().get("MYFLAG")
        self.assertEqual(
            "MYFLAG is <b>disabled</b> for all requests.", state_str(flag)
        )

    @override_settings(FLAGS={"MYFLAG": [("boolean", True)]})
    def test_state_str_bool_true(self):
        """
        Test if the condition is true.

        Args:
            self: (todo): write your description
        """
        flag = get_flags().get("MYFLAG")
        self.assertEqual(
            "MYFLAG is <b>enabled</b> for all requests.", state_str(flag)
        )
