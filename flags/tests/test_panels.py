from django.test import RequestFactory, TestCase, override_settings

from debug_toolbar.toolbar import DebugToolbar
from flags.middleware import FlagConditionsMiddleware


class FlagsPanelTestCase(TestCase):

    def setUp(self):
        self.request = RequestFactory().get('/')
        self.toolbar = DebugToolbar(self.request)
        self.toolbar.stats = {}
        self.panel = self.toolbar.get_panel_by_id('FlagsPanel')

    @override_settings(FLAGS={'MYFLAG': [('boolean', True)]})
    def test_flags_panel_has_flags_without_middleware(self):
        response = self.panel.process_request(self.request)
        self.panel.generate_stats(self.request, response)
        flags = self.panel.get_stats()['flags']
        self.assertIn('MYFLAG', [f.name for f in flags])
        self.assertIn('enabled', self.panel.content)

    @override_settings(FLAGS={'MYFLAG': [('boolean', True)]})
    def test_flags_panel_has_flags_with_middleware(self):
        self.middleware = FlagConditionsMiddleware()
        self.middleware.process_request(self.request)
        response = self.panel.process_request(self.request)
        self.panel.generate_stats(self.request, response)
        flags = self.panel.get_stats()['flags']
        self.assertIn('MYFLAG', [f.name for f in flags])
