from django.template import engines
from django.test import TestCase, override_settings


templates_override = [
    {
        'NAME': 'jinja-engine',
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'OPTIONS': {
            'extensions': [
                'flags.jinja2tags.flags',
            ],
        }
    },
]


@override_settings(
    TEMPLATES=templates_override,
    FLAGS={'MY_FLAG': {'boolean': 'True'}}
)
class FlagsExtensionTests(TestCase):
    def setUp(self):
        self.jinja_engine = engines['jinja-engine']

    def test_jinja2_flag_enabled_tag(self):
        template = self.jinja_engine.from_string(
            '{{ flag_enabled("MY_FLAG") }}'
        )
        self.assertEqual(template.render({'request': None}), 'True')

    def test_flag_disabled_tag(self):
        template = self.jinja_engine.from_string(
            '{{ flag_disabled("MY_FLAG") }}'
        )
        self.assertEqual(template.render({'request': None}), 'False')
