from django.template import engines
from django.test import TestCase, override_settings


templates_override = [
    {
        "NAME": "jinja-engine",
        "BACKEND": "django.template.backends.jinja2.Jinja2",
        "OPTIONS": {"extensions": ["flags.jinja2tags.flags"]},
    },
]


@override_settings(TEMPLATES=templates_override)
class FlagsExtensionTests(TestCase):
    def setUp(self):
        """
        Sets the engine engine.

        Args:
            self: (todo): write your description
        """
        self.jinja_engine = engines["jinja-engine"]

    def test_jinja2_flag_enabled_tag(self):
        """
        Test if a jinja2 tag templates.

        Args:
            self: (todo): write your description
        """
        template = self.jinja_engine.from_string(
            '{{ flag_enabled("FLAG_ENABLED") }}'
        )
        self.assertEqual(template.render(), "True")

    def test_jinja2_flag_disabled_tag(self):
        """
        Test for templates templates template tag

        Args:
            self: (todo): write your description
        """
        template = self.jinja_engine.from_string(
            '{{ flag_disabled("FLAG_ENABLED") }}'
        )
        self.assertEqual(template.render(), "False")

    def test_jinja2_flag_enabled_tag_with_kwarg(self):
        """
        Test if a jinja2 template tag.

        Args:
            self: (todo): write your description
        """
        template = self.jinja_engine.from_string(
            '{{ flag_enabled("FLAG_ENABLED_WITH_KWARG", passed_value=4) }}'
        )
        self.assertEqual(template.render(), "True")

    def test_jinja2_flag_disabled_tag_with_kwarg(self):
        """
        Test if a jin template tag

        Args:
            self: (todo): write your description
        """
        template = self.jinja_engine.from_string(
            '{{ flag_disabled("FLAG_ENABLED_WITH_KWARG", passed_value=4) }}'
        )
        self.assertEqual(template.render(), "False")
