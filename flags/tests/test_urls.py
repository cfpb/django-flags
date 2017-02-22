from django.conf.urls import url, include
from django.core.urlresolvers import resolve
from django.http import HttpResponse, Http404
from django.test import TestCase, RequestFactory, override_settings

from flags.urls import flagged_url
from flags.models import Flag


def view(request):
    return HttpResponse('view')


def fallback(request):
    return HttpResponse('fallback')


urlpatterns = [
    flagged_url('FLAGGED_URL', r'^url-true-no-fallback$', view,
                name='some-view', condition=True),
    flagged_url('FLAGGED_URL', r'^url-false-no-fallback$', view,
                name='some-view', condition=False),
    flagged_url('FLAGGED_URL', r'^url-true-fallback$', view,
                name='some-view', condition=True, fallback=fallback),
    flagged_url('FLAGGED_URL', r'^url-false-fallback$', view,
                name='some-view', condition=False, fallback=fallback),
]


@override_settings(ROOT_URLCONF=__name__)
class FlagCheckTestCase(TestCase):
    def setUp(self):
        self.flag_name = 'FLAGGED_URL'
        self.factory = RequestFactory()

    def test_flagged_url_true_no_fallback(self):
        Flag.objects.create(key=self.flag_name, enabled_by_default=True)

        request = self.factory.get('/url-true-no-fallback')
        resolved_view, args, kwargs = resolve('/url-true-no-fallback')
        response = resolved_view(request)

        self.assertContains(response, 'view')

    def test_flagged_url_true_no_fallback_false(self):
        Flag.objects.create(key=self.flag_name, enabled_by_default=False)

        request = self.factory.get('/url-true-no-fallback')
        resolved_view, args, kwargs = resolve('/url-true-no-fallback')

        with self.assertRaises(Http404):
            resolved_view(request)

    def test_flagged_url_false_no_fallback(self):
        Flag.objects.create(key=self.flag_name, enabled_by_default=False)

        request = self.factory.get('/url-false-no-fallback')
        resolved_view, args, kwargs = resolve('/url-false-no-fallback')
        response = resolved_view(request)

        self.assertContains(response, 'view')

    def test_flagged_url_false_no_fallback_true(self):
        Flag.objects.create(key=self.flag_name, enabled_by_default=True)

        request = self.factory.get('/url-false-no-fallback')
        resolved_view, args, kwargs = resolve('/url-false-no-fallback')

        with self.assertRaises(Http404):
            resolved_view(request)

    def test_flagged_url_true_fallback(self):
        Flag.objects.create(key=self.flag_name, enabled_by_default=True)

        request = self.factory.get('/url-true-fallback')
        resolved_view, args, kwargs = resolve('/url-true-fallback')
        response = resolved_view(request)

        self.assertContains(response, 'view')

    def test_flagged_url_true_fallback_false(self):
        Flag.objects.create(key=self.flag_name, enabled_by_default=False)

        request = self.factory.get('/url-true-fallback')
        resolved_view, args, kwargs = resolve('/url-true-fallback')
        response = resolved_view(request)

        self.assertContains(response, 'fallback')

    def test_flagged_url_false_fallback(self):
        Flag.objects.create(key=self.flag_name, enabled_by_default=False)

        request = self.factory.get('/url-false-fallback')
        resolved_view, args, kwargs = resolve('/url-false-fallback')
        response = resolved_view(request)

        self.assertContains(response, 'view')

    def test_flagged_url_false_fallback_false(self):
        Flag.objects.create(key=self.flag_name, enabled_by_default=True)

        request = self.factory.get('/url-false-fallback')
        resolved_view, args, kwargs = resolve('/url-false-fallback')
        response = resolved_view(request)

        self.assertContains(response, 'fallback')

    def test_flagged_url_include(self):
        with self.assertRaises(TypeError):
            flagged_url('MY_FLAG', r'^my_url/$', include([
                url(r'^my_included_url', view)
            ]))

    def test_flagged_url_not_callable(self):
        with self.assertRaises(TypeError):
            flagged_url('MY_FLAG', r'^my_url/$', 'string')
