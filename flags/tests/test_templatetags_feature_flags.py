from django.http import HttpRequest
from django.template import Context, Template
from django.test import TestCase


class FlagsTemplateTagsTestCase(TestCase):
    def setUp(self):
        """
        Sets the request.

        Args:
            self: (todo): write your description
        """
        self.request = HttpRequest()

    def render_template(self, string, context=None):
        """
        Render a template. template.

        Args:
            self: (todo): write your description
            string: (str): write your description
            context: (todo): write your description
        """
        context = context or {"request": self.request}
        context = Context(context)
        return Template(string).render(context)

    def test_flag_enabled_disabled(self):
        """
        Check if enabled enabled enabled enabled.

        Args:
            self: (todo): write your description
        """
        rendered = self.render_template(
            "{% load feature_flags %}"
            '{% flag_enabled "FLAG_DISABLED" as test_flag %}'
            "{% if test_flag %}"
            "flag enabled"
            "{% else %}"
            "flag disabled"
            "{% endif %}"
        )
        self.assertEqual(rendered, "flag disabled")

    def test_flag_enabled_does_not_exist(self):
        """
        Test if the test test is enabled.

        Args:
            self: (todo): write your description
        """
        # Disabled can also mean non-existent
        rendered = self.render_template(
            "{% load feature_flags %}"
            '{% flag_enabled "FLAG_DOES_NOT_EXIST" as test_flag %}'
            "{% if test_flag %}"
            "flag enabled"
            "{% else %}"
            "flag disabled"
            "{% endif %}"
        )
        self.assertEqual(rendered, "flag disabled")

    def test_flag_enabled_enabled(self):
        """
        Check if enabled enabled enabled enabled.

        Args:
            self: (todo): write your description
        """
        rendered = self.render_template(
            "{% load feature_flags %}"
            '{% flag_enabled "FLAG_ENABLED" as test_flag %}'
            "{% if test_flag %}"
            "flag enabled"
            "{% else %}"
            "flag disabled"
            "{% endif %}"
        )
        self.assertEqual(rendered, "flag enabled")

    def test_flag_enabled_no_request(self):
        """
        Displays the test request.

        Args:
            self: (todo): write your description
        """
        rendered = self.render_template(
            "{% load feature_flags %}"
            '{% flag_enabled "FLAG_ENABLED" as test_flag %}'
            "{% if test_flag %}"
            "flag enabled"
            "{% else %}"
            "flag disabled"
            "{% endif %}",
            context={},
        )
        self.assertEqual(rendered, "flag enabled")

    def test_flag_enabled_with_kwarg(self):
        """
        Test if the test flag is enabled.

        Args:
            self: (todo): write your description
        """
        rendered = self.render_template(
            "{% load feature_flags %}"
            '{% flag_enabled "FLAG_ENABLED_WITH_KWARG" passed_value=4 as test_flag %}'  # noqa 502
            "{% if test_flag %}"
            "flag enabled"
            "{% else %}"
            "flag disabled"
            "{% endif %}"
        )
        self.assertEqual(rendered, "flag enabled")

    def test_flag_disabled_disabled(self):
        """
        Test if the test test template is disabled.

        Args:
            self: (todo): write your description
        """
        # Disabled can also mean non-existent
        rendered = self.render_template(
            "{% load feature_flags %}"
            '{% flag_disabled "FLAG_DISABLED" as test_flag %}'
            "{% if test_flag %}"
            "flag disabled"
            "{% else %}"
            "flag enabled"
            "{% endif %}"
        )
        self.assertEqual(rendered, "flag disabled")

    def test_flag_disabled_no_request(self):
        """
        This view for test.

        Args:
            self: (todo): write your description
        """
        # Disabled can also mean non-existent
        rendered = self.render_template(
            "{% load feature_flags %}"
            '{% flag_disabled "FLAG_DISABLED" as test_flag %}'
            "{% if test_flag %}"
            "flag disabled"
            "{% else %}"
            "flag enabled"
            "{% endif %}",
            context={},
        )
        self.assertEqual(rendered, "flag disabled")

    def test_flag_disabled_with_kwarg(self):
        """
        Determine whether the test test test is enabled.

        Args:
            self: (todo): write your description
        """
        rendered = self.render_template(
            "{% load feature_flags %}"
            '{% flag_disabled "FLAG_ENABLED_WITH_KWARG" passed_value=4 as test_flag %}'  # noqa 502
            "{% if test_flag %}"
            "flag enabled"
            "{% else %}"
            "flag disabled"
            "{% endif %}"
        )
        self.assertEqual(rendered, "flag disabled")

    def test_flag_disabled_does_not_exist(self):
        """
        Check if the test test test test is enabled.

        Args:
            self: (todo): write your description
        """
        rendered = self.render_template(
            "{% load feature_flags %}"
            '{% flag_disabled "FLAG_DOES_NOT_EXIST" as test_flag %}'
            "{% if test_flag %}"
            "flag disabled"
            "{% else %}"
            "flag enabled"
            "{% endif %}"
        )
        self.assertEqual(rendered, "flag disabled")

    def test_flag_disabled_enabled(self):
        """
        Check if the test test is enabled.

        Args:
            self: (todo): write your description
        """
        rendered = self.render_template(
            "{% load feature_flags %}"
            '{% flag_disabled "FLAG_ENABLED" as test_flag %}'
            "{% if test_flag %}"
            "flag disabled"
            "{% else %}"
            "flag enabled"
            "{% endif %}"
        )
        self.assertEqual(rendered, "flag enabled")
