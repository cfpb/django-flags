from django.core.exceptions import ImproperlyConfigured
from django.http import Http404, HttpRequest, HttpResponse
from django.test import TestCase, override_settings
from django.views.generic import View

from flags.views import FlaggedViewMixin


class TestView(FlaggedViewMixin, View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('ok')


class FlaggedViewMixinTestCase(TestCase):
    def setUp(self):
        self.flag_name = 'FLAGGED_VIEW_MIXIN'

    def request(self, path='/'):
        request = HttpRequest()

        request.method = 'GET'
        request.path = path
        request.META['SERVER_NAME'] = 'localhost'
        request.META['SERVER_PORT'] = 8000

        return request

    def test_no_flag_key_raises_improperly_configured(self):
        view = TestView.as_view()
        self.assertRaises(ImproperlyConfigured, view, self.request())

    def test_no_flag_acts_as_disabled(self):
        view = TestView.as_view(flag_name=self.flag_name)
        self.assertRaises(Http404, view, self.request())

    @override_settings(FLAGS={'FLAGGED_VIEW_MIXIN': {'boolean': True}})
    def test_flag_set_view_enabled(self):
        view = TestView.as_view(flag_name=self.flag_name)
        self.assertEqual(view(self.request()).status_code, 200)

    @override_settings(FLAGS={'FLAGGED_VIEW_MIXIN': {'boolean': False}})
    def test_flag_set_view_disabled(self):
        view = TestView.as_view(flag_name=self.flag_name)
        self.assertRaises(Http404, view, self.request())

    def test_fallback_view_function_disabled(self):
        def test_view_function(request, *args, **kwargs):
            return HttpResponse('fallback fn')

        view = TestView.as_view(
            flag_name=self.flag_name,
            condition=True,
            fallback=test_view_function
        )

        response = view(self.request())
        self.assertContains(response, 'fallback fn')

    @override_settings(FLAGS={'FLAGGED_VIEW_MIXIN': {'boolean': True}})
    def test_fallback_view_function_enabled(self):
        def test_view_function(request, *args, **kwargs):
            return HttpResponse('fallback fn')

        view = TestView.as_view(
            flag_name=self.flag_name,
            condition=True,
            fallback=test_view_function
        )

        response = view(self.request())
        self.assertContains(response, 'ok')

    def test_fallback_class_based_view(self):
        class OtherTestView(View):
            def get(self, request, *args, **kwargs):
                return HttpResponse('fallback cbv')

        view = TestView.as_view(
            flag_name=self.flag_name,
            condition=True,
            fallback=OtherTestView.as_view()
        )

        response = view(self.request())
        self.assertContains(response, 'fallback cbv')
