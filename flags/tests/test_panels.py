from django.http import HttpResponse
from django.test import RequestFactory, TestCase, override_settings

from debug_toolbar.toolbar import DebugToolbar

from flags.state import flag_state


class FlagsPanelTestCase(TestCase):
    def setUp(self):
        self.request = RequestFactory().get("/")
        self.get_response = lambda req: HttpResponse()
        self.toolbar = DebugToolbar(self.request, self.get_response)
        self.toolbar.stats = {}
        self.panel = self.toolbar.get_panel_by_id("FlagsPanel")

    @override_settings(FLAGS={"MYFLAG": [("boolean", True)]})
    def test_flags_panel_has_flags(self):
        response = self.panel.process_request(self.request)
        self.panel.generate_stats(self.request, response)
        flags = self.panel.get_stats()["flags"]
        self.assertIn("MYFLAG", [f.name for f in flags])
        self.assertIn("enabled", self.panel.content)


class FlagChecksPanelTestCase(TestCase):
    def setUp(self):
        self.request = RequestFactory().get("/")
        self.get_response = lambda req: HttpResponse()
        self.toolbar = DebugToolbar(self.request, self.get_response)
        self.toolbar.stats = {}
        self.panel = self.toolbar.get_panel_by_id("FlagChecksPanel")

    @override_settings(FLAGS={"MYFLAG": [("boolean", True)]})
    def test_recording(self):
        self.assertEqual(len(self.panel.checks), 0)

        self.panel.enable_instrumentation()
        flag_state("MYFLAG")
        self.panel.disable_instrumentation()

        self.assertEqual(len(self.panel.checks), 1)

        response = self.panel.process_request(self.request)
        self.panel.generate_stats(self.request, response)
        checks = self.panel.get_stats()["checks"]

        self.assertIn("MYFLAG", checks)
        self.assertEqual([True], checks["MYFLAG"])
