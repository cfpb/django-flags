from django.http import HttpRequest
from django.template import Context, Template
from django.test import TestCase


class FlagsTemplateTagsTestCase(TestCase):

    def setUp(self):
        self.request = HttpRequest()

    def render_template(self, string, context=None):
        context = context or {'request': self.request}
        context = Context(context)
        return Template(string).render(context)

    def test_flag_enabled_disabled(self):
        rendered = self.render_template(
            '{% load feature_flags %}'
            '{% flag_enabled "FLAG_DISABLED"  as test_flag %}'
            '{% if test_flag %}'
            'flag enabled'
            '{% else %}'
            'flag disabled'
            '{% endif %}'
        )
        self.assertEqual(rendered, 'flag disabled')

    def test_flag_enabled_does_not_exist(self):
        # Disabled can also mean non-existent
        rendered = self.render_template(
            '{% load feature_flags %}'
            '{% flag_enabled "FLAG_DOES_NOT_EXIST"  as test_flag %}'
            '{% if test_flag %}'
            'flag enabled'
            '{% else %}'
            'flag disabled'
            '{% endif %}'
        )
        self.assertEqual(rendered, 'flag disabled')

    def test_flag_enabled_enabled(self):
        rendered = self.render_template(
            '{% load feature_flags %}'
            '{% flag_enabled "FLAG_ENABLED"  as test_flag %}'
            '{% if test_flag %}'
            'flag enabled'
            '{% else %}'
            'flag disabled'
            '{% endif %}'
        )
        self.assertEqual(rendered, 'flag enabled')

    def test_flag_disabled_disabled(self):
        # Disabled can also mean non-existent
        rendered = self.render_template(
            '{% load feature_flags %}'
            '{% flag_disabled "FLAG_DISABLED"  as test_flag %}'
            '{% if test_flag %}'
            'flag disabled'
            '{% else %}'
            'flag enabled'
            '{% endif %}'
        )
        self.assertEqual(rendered, 'flag disabled')

    def test_flag_disabled_does_not_exist(self):
        rendered = self.render_template(
            '{% load feature_flags %}'
            '{% flag_disabled "FLAG_DOES_NOT_EXIST"  as test_flag %}'
            '{% if test_flag %}'
            'flag disabled'
            '{% else %}'
            'flag enabled'
            '{% endif %}'
        )
        self.assertEqual(rendered, 'flag disabled')

    def test_flag_disabled_enabled(self):
        rendered = self.render_template(
            '{% load feature_flags %}'
            '{% flag_disabled "FLAG_ENABLED"  as test_flag %}'
            '{% if test_flag %}'
            'flag disabled'
            '{% else %}'
            'flag enabled'
            '{% endif %}'
        )
        self.assertEqual(rendered, 'flag enabled')
