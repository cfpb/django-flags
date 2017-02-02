from django.core.exceptions import ImproperlyConfigured
from django.http import Http404, HttpRequest, HttpResponse
from django.test import TestCase
from django.views.generic import View
from wagtail.wagtailcore.models import Page, Site
from wagtail.wagtailcore.views import serve as wagtail_serve

from flags.models import Flag
from flags.views import FlaggedViewMixin


class TestView(FlaggedViewMixin, View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('ok')


class FlaggedViewMixinTestCase(TestCase):
    def setUp(self):
        self.flag_name = 'FLAGGED_VIEW_MIXIN_TEST_CASE'

    def request(self, path='/'):
        request = HttpRequest()

        request.method = 'GET'
        request.path = path
        request.META['SERVER_NAME'] = 'localhost'
        request.META['SERVER_PORT'] = 8000
        request.site = Site.objects.get(is_default_site=True)

        return request

    def test_no_flag_key_raises_improperly_configured(self):
        view = TestView.as_view()
        self.assertRaises(ImproperlyConfigured, view, self.request())

    def test_no_flag_acts_as_disabled(self):
        view = TestView.as_view(flag_name=self.flag_name)
        self.assertRaises(Http404, view, self.request())

    def test_flag_set_view_enabled(self):
        Flag.objects.create(key=self.flag_name, enabled_by_default=True)
        view = TestView.as_view(flag_name=self.flag_name)
        self.assertEqual(view(self.request()).status_code, 200)

    def test_flag_set_view_disabled(self):
        Flag.objects.create(key=self.flag_name, enabled_by_default=False)
        view = TestView.as_view(flag_name=self.flag_name)
        self.assertRaises(Http404, view, self.request())

    def test_fallback_view_function_disabled(self):
        def test_view_function(request, *args, **kwargs):
            return HttpResponse('fallback fn')

        view = TestView.as_view(
            flag_name=self.flag_name,
            fallback_view=test_view_function
        )

        response = view(self.request())
        if isinstance(response.content, str):
            content = response.content
        else:
            content = bytes.decode(response.content)
        self.assertEqual(content, 'fallback fn')

    def test_fallback_view_function_enabled(self):
        def test_view_function(request, *args, **kwargs):
            return HttpResponse('fallback fn')

        Flag.objects.create(key=self.flag_name, enabled_by_default=True)
        view = TestView.as_view(
            flag_name=self.flag_name,
            fallback_view=test_view_function
        )

        response = view(self.request())
        if isinstance(response.content, str):
            content = response.content
        else:
            content = bytes.decode(response.content)
        self.assertEqual(content, 'ok')

    def test_fallback_class_based_view(self):
        class OtherTestView(View):
            def get(self, request, *args, **kwargs):
                return HttpResponse('fallback cbv')

        view = TestView.as_view(
            flag_name=self.flag_name,
            fallback_view=OtherTestView.as_view()
        )

        response = view(self.request())
        if isinstance(response.content, str):
            content = response.content
        else:
            content = bytes.decode(response.content)
        self.assertEqual(content, 'fallback cbv')

    def test_fallback_wagtail_serve(self):
        site = Site.objects.get(is_default_site=True)
        root = site.root_page
        page = Page(title='wagtail title', slug='title')
        root.add_child(instance=page)
        page.save()
        page.save_revision().publish()

        fail_through = lambda request: wagtail_serve(request, request.path)
        view = TestView.as_view(flag_name=self.flag_name,
                                fallback_view=fail_through)

        response = view(self.request(path='/title'))
        self.assertContains(response, '<title>wagtail title</title>')
